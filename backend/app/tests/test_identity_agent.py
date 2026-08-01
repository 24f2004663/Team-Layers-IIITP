import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock

from app.ai.graph.events import SystemEvent
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.ai.graph.workflow import WorkflowStage
from app.ai.agents.identity.agent import IdentityAgent
from app.ai.agents.identity.schemas import IdentityProfile
from app.ai.framework.messages import AIResponse
from app.ai.llm.factory import llm_factory
from app.ai.framework.errors import ValidationError

# Mock LLM response string
MOCK_JSON_OUTPUT = """
{
  "identity_summary": "Aspiring AI Engineer dedicated to crafting robust systems",
  "career_goal": "Lead AI Architect",
  "mission": "To scale agentic solutions with clean code",
  "core_values": ["Growth", "Precision"],
  "interests": ["Python", "Machine Learning"],
  "strengths": ["Clean Code", "Design Patterns"],
  "weaknesses": ["Impatient"],
  "learning_style": "Visual",
  "preferred_difficulty": "Hard",
  "time_commitment": "10 hours/week",
  "motivation_level": "High",
  "confidence_score": 0.95
}
"""

class MockMemoryManager:
    """Mock database memory manager for identity tests."""
    def __init__(self):
        self.db = {}

    async def load(self, user_id):
        return self.db.get(user_id, {"goals": [], "skills": [], "timeline": []})

    async def save(self, user_id, data):
        self.db[user_id] = data
        return True

    async def update(self, user_id, data):
        if user_id not in self.db:
            self.db[user_id] = {}
        self.db[user_id].update(data)
        return True

    async def delete(self, user_id):
        if user_id in self.db:
            del self.db[user_id]
        return True

@pytest.fixture
def mock_gemini():
    """Fixture to patch llm_factory returning a mock LLM."""
    mock_llm = MagicMock()
    mock_llm.invoke = AsyncMock(return_value=AIResponse(
        content=MOCK_JSON_OUTPUT,
        latency=0.04,
        cost=0.001,
        finish_reason="stop"
    ))
    original_get_llm = llm_factory.get_llm
    llm_factory.get_llm = lambda provider: mock_llm
    yield mock_llm
    llm_factory.get_llm = original_get_llm

@pytest.mark.asyncio
async def test_identity_agent_profile_creation(mock_gemini):
    from app.ai.runtime.container import container
    mem_manager = MockMemoryManager()
    container.identity_memory = mem_manager
    
    agent = IdentityAgent()
    
    # 1. Setup State for USER_ONBOARDED
    state = LifeGPSState(
        event={
            "event_type": SystemEvent.USER_ONBOARDED,
            "payload": {
                "goals": ["Become a senior developer"],
                "interests": ["Backend Engineering"]
            }
        },
        session={"session_id": uuid4(), "client_platform": "windows"},
        user={"user_id": uuid4()}
    )
    
    context = ExecutionContext(
        workflow_id=uuid4(),
        execution_id=uuid4(),
        event=SystemEvent.USER_ONBOARDED,
        current_stage=WorkflowStage.ANALYSIS,
        current_agent="IdentityAgent"
    )
    
    # 2. Run agent execution pipeline
    result = await agent.execute(state, context)
    
    # 3. Assertions
    assert result.success
    assert result.explanation is not None
    assert result.explanation["timeline_changes"]["career_goal"] == "Lead AI Architect"
    assert state.identity.archetype == "Aspiring AI Engineer dedicated to crafting robust systems"
    
    # Verify database updates
    saved_data = mem_manager.db[state.user.user_id]
    assert saved_data["career_goal"] == "Lead AI Architect"
    assert len(saved_data["timeline"]) == 1
    assert saved_data["timeline"][0]["reason_for_change"] == "Onboarding completed"

@pytest.mark.asyncio
async def test_identity_agent_profile_update(mock_gemini):
    from app.ai.runtime.container import container
    mem_manager = MockMemoryManager()
    container.identity_memory = mem_manager
    
    agent = IdentityAgent()
    
    # Setup State for PROFILE_UPDATED
    state = LifeGPSState(
        event={
            "event_type": SystemEvent.PROFILE_UPDATED,
            "payload": {
                "goals": ["Become a manager"],
                "interests": ["Team Leadership"]
            }
        },
        session={"session_id": uuid4(), "client_platform": "windows"},
        user={"user_id": uuid4()}
    )
    
    context = ExecutionContext(
        workflow_id=uuid4(),
        execution_id=uuid4(),
        event=SystemEvent.PROFILE_UPDATED,
        current_stage=WorkflowStage.ANALYSIS,
        current_agent="IdentityAgent"
    )
    
    result = await agent.execute(state, context)
    
    assert result.success
    saved_data = mem_manager.db[state.user.user_id]
    assert saved_data["timeline"][0]["reason_for_change"] == "User profile update requested"

@pytest.mark.asyncio
async def test_identity_agent_validation_failure():
    agent = IdentityAgent()
    
    # Create invalid profile lacking career goal
    invalid_profile = IdentityProfile(
        identity_summary="test",
        career_goal="",  # Empty career goal fails validation
        mission="test",
        core_values=[],
        interests=["Python"],
        strengths=[],
        weaknesses=[],
        confidence_score=0.9
    )
    
    # Should raise ValidationError
    with pytest.raises(ValidationError):
        agent.validator.validate(invalid_profile)
