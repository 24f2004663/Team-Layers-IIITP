import pytest
from uuid import uuid4
from unittest.mock import MagicMock, AsyncMock

from app.ai.graph.events import SystemEvent
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.ai.graph.workflow import WorkflowStage
from app.ai.agents.gap_analysis.agent import GapAnalysisAgent
from app.ai.agents.gap_analysis.schemas import GapAnalysisResult
from app.ai.agents.gap_analysis.decision_engine import DecisionEngine
from app.ai.framework.messages import AIResponse
from app.ai.llm.factory import llm_factory

class MockMemoryManager:
    def __init__(self):
        self.db = {}

    async def load(self, user_id):
        return self.db.get(user_id, {"gap_history": [], "consistency_score": 0.6, "focus_style": "Spurt"})

    async def save(self, user_id, data):
        self.db[user_id] = data
        return True

    async def update(self, user_id, data):
        if user_id not in self.db:
            self.db[user_id] = {}
        self.db[user_id].update(data)
        return True

MOCK_JSON_OUTPUT = """
{
  "overall_gap_score": 0.35,
  "priority_gaps": [
    {
      "category": "Consistency Gap",
      "severity": "Medium",
      "confidence": 0.85,
      "supporting_observations": ["Study consistency dropped from baseline of 0.8 to 0.6"],
      "affected_goals": ["Become AI Engineer"]
    }
  ],
  "behavior_conflicts": ["Target consistency values do not align with actual study metrics"],
  "identity_alignment": 0.75,
  "critical_risks": ["High procrastination risk on hard coding milestones"],
  "growth_strengths": ["Strong focus span when session is initiated"],
  "recommended_strategy": "Consistency First",
  "confidence": 0.90,
  "reasoning": "User has high aspirations but struggles with consistency.",
  "decision_trace": {
    "input_signals": ["identity_profile", "behavior_profile"],
    "reasoning_steps": ["Compares goals vs consistency score", "Checks procrastination levels"],
    "evidence_used": ["consistency_score=0.60"],
    "confidence": 0.95,
    "tradeoffs": ["Selected consistency focus over deep work focus"]
  }
}
"""

@pytest.fixture
def mock_gemini():
    mock_llm = MagicMock()
    mock_llm.invoke = AsyncMock(return_value=AIResponse(
        content=MOCK_JSON_OUTPUT,
        latency=0.03,
        cost=0.001,
        finish_reason="stop"
    ))
    original_get_llm = llm_factory.get_llm
    llm_factory.get_llm = lambda provider: mock_llm
    yield mock_llm
    llm_factory.get_llm = original_get_llm

@pytest.mark.asyncio
async def test_gap_analysis_workflow(mock_gemini):
    from app.ai.runtime.container import container
    mem_manager = MockMemoryManager()
    container.behavior_memory = mem_manager
    container.identity_memory = mem_manager
    
    agent = GapAnalysisAgent()
    
    state = LifeGPSState(
        event={"event_type": SystemEvent.PROFILE_UPDATED, "payload": {}},
        session={"session_id": uuid4(), "client_platform": "windows"},
        user={"user_id": uuid4()}
    )
    
    context = ExecutionContext(
        workflow_id=uuid4(),
        execution_id=uuid4(),
        event=SystemEvent.PROFILE_UPDATED,
        current_stage=WorkflowStage.ANALYSIS,
        current_agent="GapAnalysisAgent"
    )
    
    result = await agent.execute(state, context)
    
    assert result.success
    assert result.explanation is not None
    assert result.explanation["overall_gap_score"] == 0.35
    assert "decision_priority" in result.explanation
    
    # Priority Graph check
    priority = result.explanation["decision_priority"]
    assert priority["primary_priority"] == "Consistency"
    assert len(priority["priority_graph"]["nodes"]) == 4
