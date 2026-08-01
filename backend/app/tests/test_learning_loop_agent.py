import pytest
from uuid import uuid4
from unittest.mock import MagicMock, AsyncMock

from app.ai.graph.events import SystemEvent
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.ai.graph.workflow import WorkflowStage
from app.ai.agents.learning_loop.agent import LearningLoopAgent
from app.ai.agents.learning_loop.schemas import LearningLoopAgentOutput
from app.ai.framework.messages import AIResponse
from app.ai.llm.factory import llm_factory

class MockMemoryManager:
    def __init__(self):
        self.db = {}

    async def load(self, user_id):
        return self.db.get(user_id, {
            "reflections_history": [], "growth_history": [], "calibration_history": [],
            "growth_timeline": [], "identity_evolution_graph": []
        })

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
  "reflection": {
    "daily_reflection": "Excellent progress today. Completed all core syntax exercises with high focus levels.",
    "weekly_reflection": "Consistency is improving. Reached Q1 Q2 milestones on track.",
    "mission_reflection": "Strong alignment with Q1 target to acquire programming fundamentals.",
    "learning_reflection": "Concepts loops are mastered; move on to NumPy vectors.",
    "behavior_reflection": "Low distractions during morning slots.",
    "identity_reflection": "User is actively evolving toward a capable AI engineer identity.",
    "quality_score": {
      "evidence_coverage": 0.95,
      "reasoning_quality": 0.90,
      "actionability": 0.88,
      "confidence": 0.92,
      "completeness": 0.95
    }
  },
  "growth_delta": {
    "yesterday_consistency": 0.60,
    "today_consistency": 0.68,
    "yesterday_focus_minutes": 60,
    "today_focus_minutes": 90,
    "consistency_delta": 0.08,
    "focus_delta": 30,
    "learning_velocity_delta": 0.12
  },
  "resource_effectiveness": [
    {
      "resource_type": "Video",
      "learning_gain": 0.85,
      "retention": 0.80,
      "completion": 0.95,
      "enjoyment": 0.90
    }
  ],
  "simulator_calibration": {
    "predicted_outcome_probability": 0.80,
    "actual_outcome_probability": 0.85,
    "calibration_factor": 1.06,
    "updated_weight": 0.85
  },
  "counterfactuals": [
    {
      "change": "If you had studied 20 more minutes",
      "expected_delta": 0.14,
      "confidence": 0.85
    }
  ],
  "interventions": [
    {
      "trigger": "Sleep drop",
      "recommendation": "22:30 screen downtime block limit",
      "expected_effect": 0.12,
      "priority": 0.90
    }
  ],
  "growth_index": {
    "focus": 0.85,
    "consistency": 0.75,
    "learning_velocity": 0.80,
    "skill_gain": 0.90,
    "identity_alignment": 0.92,
    "mission_completion": 0.80,
    "momentum": 0.85,
    "composite_index": 0.84
  },
  "decision_memory": {
    "decision_id": "00000000-0000-0000-0000-000000000000",
    "outcome_description": "Morning study slot suggestion resulted in successful Q1 milestones completed",
    "success_rating": 0.95,
    "future_weight": 0.92
  },
  "identity_graph": {
    "nodes": [
      {
        "state_name": "Data Analyst",
        "confidence": 0.90,
        "transition_timestamp": "2026-08-01T09:00:00Z"
      },
      {
        "state_name": "ML Engineer",
        "confidence": 0.85,
        "transition_timestamp": "2026-08-01T12:00:00Z"
      },
      {
        "state_name": "AI Engineer",
        "confidence": 0.71,
        "transition_timestamp": "2026-08-01T15:00:00Z"
      }
    ]
  },
  "weekly_trajectory": {
    "target_identity": "AI Engineer",
    "current_match_percentage": 0.71,
    "previous_match_percentage": 0.67,
    "change_percentage": 0.04
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
async def test_learning_loop_workflow(mock_gemini):
    from app.ai.runtime.container import container
    mem_manager = MockMemoryManager()
    container.behavior_memory = mem_manager
    container.identity_memory = mem_manager
    
    agent = LearningLoopAgent()
    
    state = LifeGPSState(
        event={"event_type": SystemEvent.REFLECTION_SUBMITTED, "payload": {}},
        session={"session_id": uuid4(), "client_platform": "windows"},
        user={"user_id": uuid4()}
    )
    
    context = ExecutionContext(
        workflow_id=uuid4(),
        execution_id=uuid4(),
        event=SystemEvent.REFLECTION_SUBMITTED,
        current_stage=WorkflowStage.ANALYSIS,
        current_agent="LearningLoopAgent"
    )
    
    result = await agent.execute(state, context)
    
    assert result.success
    assert result.explanation is not None
    assert result.explanation["growth_index"] == 0.84
    assert len(result.explanation["interventions"]) == 1
