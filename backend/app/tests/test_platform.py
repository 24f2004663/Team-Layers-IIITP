import pytest
import os
from uuid import uuid4
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from app.ai.prompts.loader import PromptLoader
from app.ai.prompts.registry import PromptRegistry
from app.ai.prompts.base import PromptMetadata
from app.ai.parser.json_parser import JSONParser
from app.ai.parser.repair import JSONRepair
from app.ai.parser.response_mapper import ResponseMapper
from app.ai.validator.schema_validator import SchemaValidator
from app.ai.validator.confidence_validator import ConfidenceValidator
from app.ai.framework.memory_adapter import MemoryAdapter
from app.ai.framework.agent_runtime import AgentRuntime, Explanation
from app.ai.framework.messages import AIMessage, AIResponse
from app.ai.agents.base.agent import BaseAgent, AgentMetadata
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.ai.graph.events import SystemEvent
from app.ai.graph.workflow import WorkflowStage
from app.ai.graph.contracts import AgentResult

# 1. Pydantic test models
class DummySchema(BaseModel):
    archetype: str
    core_values: List[str]
    strengths: List[str]
    weaknesses: List[str]

class MockMemoryManager:
    """Mock database memory manager for tests."""
    def __init__(self):
        self.db = {}

    async def load(self, user_id):
        return self.db.get(user_id, {"goals": [], "skills": []})

    async def save(self, user_id, data):
        self.db[user_id] = data
        return True

    async def update(self, user_id, data):
        self.db[user_id].update(data)
        return True

    async def delete(self, user_id):
        if user_id in self.db:
            del self.db[user_id]
        return True

# 2. Prompts Tests
def test_prompt_loader_and_registry():
    base_dir = os.path.dirname(os.path.dirname(__file__)) + "/ai/prompts"
    loader = PromptLoader(base_dir)
    registry = PromptRegistry(loader)
    
    # Load identity prompt
    prompt = registry.get_prompt("identity", "v1")
    assert prompt.metadata.name == "Identity Profiling Prompt"
    assert "{goals}" in prompt.template
    
    # Check fallback versioning: get missing v2 falls back to v1
    fallback = registry.get_prompt("identity", "v2")
    assert fallback.metadata.version == "v1"

# 3. JSON Parser & Repair Tests
def test_json_parser_and_repair():
    parser = JSONParser()
    repair = JSONRepair()
    mapper = ResponseMapper()
    
    # Standard JSON parse
    text_normal = '{"archetype": "Architect", "core_values": ["Growth"], "strengths": ["Logic"], "weaknesses": ["None"]}'
    res = parser.parse(text_normal)
    assert res["archetype"] == "Architect"
    
    # Malformed JSON with markdown wrapping
    text_markdown = '```json\n{"archetype": "Strategist", "core_values": ["Design"], "strengths": ["Strategy"], "weaknesses": ["None"]}\n```'
    res_md = parser.parse(text_markdown)
    assert res_md["archetype"] == "Strategist"
    
    # Malformed JSON requiring repair (missing brackets/braces/quotes)
    malformed = '{"archetype": "Leader", "core_values": ["Empowerment"], "strengths": ["Vision"], "weaknesses": ["Impatient"'
    repaired = repair.repair_json_string(malformed)
    assert repaired.endswith("}") or repaired.endswith('"}')
    
    parsed_model = mapper.map_response(malformed, DummySchema)
    assert parsed_model.archetype == "Leader"

# 4. Validators Tests
def test_validators():
    schema_val = SchemaValidator()
    conf_val = ConfidenceValidator(min_confidence=0.75)
    
    dummy = DummySchema(archetype="a", core_values=["b"], strengths=["c"], weaknesses=["d"])
    assert schema_val.validate_schema(dummy)
    assert conf_val.validate_confidence(0.85)
    assert not conf_val.validate_confidence(0.60)

# 5. Memory Adapter Tests
@pytest.mark.asyncio
async def test_memory_adapter():
    manager = MockMemoryManager()
    adapter = MemoryAdapter(manager)
    uid = uuid4()
    
    # Load default
    val = await adapter.load_memory(uid)
    assert val == {"goals": [], "skills": []}
    
    # Save & Snapshot
    await adapter.save_memory(uid, {"goals": ["Learn AI"], "skills": ["Python"]})
    snap = await adapter.snapshot(uid)
    assert snap["goals"] == ["Learn AI"]
    
    # Update & Diff
    await adapter.update_memory(uid, {"skills": ["Python", "Rust"]})
    diff_val = await adapter.diff(uid, snap)
    assert "skills" in diff_val
    
    # Rollback
    await adapter.rollback(uid, snap)
    rolled = await adapter.load_memory(uid)
    assert rolled["skills"] == ["Python"]

# 6. Pipeline/Runtime Tests
class DummyPlatformAgent(BaseAgent):
    async def initialize(self) -> None:
        pass

    async def validate(self, state: LifeGPSState) -> bool:
        return True

    async def cleanup(self) -> None:
        pass

@pytest.mark.asyncio
async def test_agent_runtime():
    from unittest.mock import MagicMock, AsyncMock
    from app.ai.llm.factory import llm_factory
    
    mock_llm = MagicMock()
    mock_llm.invoke = AsyncMock(return_value=AIResponse(
        content="mocked output",
        latency=0.05,
        cost=0.001,
        finish_reason="stop"
    ))
    
    original_get_llm = llm_factory.get_llm
    llm_factory.get_llm = lambda provider: mock_llm
    
    try:
        agent = DummyPlatformAgent(
            AgentMetadata(
                name="DummyPlatformAgent",
                description="Testing agent runtime pipeline",
                capabilities=["TEST_CAP"],
                supported_events=[SystemEvent.USER_LOGIN],
                required_memory=[],
                stage=WorkflowStage.ANALYSIS
            )
        )
        
        state = LifeGPSState(
            event={"event_type": SystemEvent.USER_LOGIN, "payload": {}},
            session={"session_id": uuid4(), "client_platform": "windows"},
            user={"user_id": uuid4()}
        )
        
        context = ExecutionContext(
            workflow_id=uuid4(),
            execution_id=uuid4(),
            event=SystemEvent.USER_LOGIN,
            current_stage=WorkflowStage.ANALYSIS,
            current_agent="DummyPlatformAgent"
        )
        
        runtime = AgentRuntime()
        result = await runtime.run(agent, state, context)
        
        assert result.success
        assert result.explanation is not None
        assert result.explanation["confidence"] == 0.90
    finally:
        llm_factory.get_llm = original_get_llm
