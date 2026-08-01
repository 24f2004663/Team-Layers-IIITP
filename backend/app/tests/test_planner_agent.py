import pytest
from uuid import uuid4
from unittest.mock import MagicMock, AsyncMock

from app.ai.graph.events import SystemEvent
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.ai.graph.workflow import WorkflowStage
from app.ai.agents.planner.agent import PlannerAgent
from app.ai.agents.planner.schemas import PlannerAgentOutput, ExecutionPlanItem
from app.ai.agents.planner.adaptive_scheduler import AdaptiveScheduler
from app.ai.framework.messages import AIResponse
from app.ai.llm.factory import llm_factory

class MockMemoryManager:
    def __init__(self):
        self.db = {}

    async def load(self, user_id):
        return self.db.get(user_id, {"plans_history": [], "plans_timeline": []})

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

MOCK_JSON_OUTPUT = """
{
  "execution_plan": {
    "target_date": "2026-08-01",
    "units_sequence": [
      {
        "unit_id": "00000000-0000-0000-0000-000000000000",
        "mission_id": "00000000-0000-0000-0000-000000000000",
        "title": "Review variables and data structures basics",
        "estimated_duration": 20,
        "priority": 0.90
      }
    ],
    "health_score": {
      "workload_balance": 0.90,
      "energy_match": 0.85,
      "focus_match": 0.95,
      "dependency_integrity": 1.0,
      "estimated_success_probability": 0.92
    }
  },
  "calendar_plan": {
    "target_date": "2026-08-01",
    "agenda": [
      {
        "unit_id": "00000000-0000-0000-0000-000000000000",
        "title": "Review variables and data structures basics",
        "start_time": "2026-08-01T09:00:00Z",
        "end_time": "2026-08-01T09:20:00Z",
        "focus_window": "Morning",
        "explanation": {
          "why_this_mission": "Highest priority prerequisite syntax task",
          "why_this_time": "Aligned with user peak morning hours (9am)",
          "why_this_order": "Prerequisites scheduled first",
          "supporting_gap": "Prerequisite gap",
          "supporting_strategy": "Tiny Habits",
          "expected_outcome": "Solid syntax fundamentals",
          "confidence": 0.95,
          "deferred_reason": "Not deferred",
          "skipped_risk": "High risk of delaying milestone",
          "alternative_schedule": "09:30:00Z"
        }
      }
    ],
    "total_focused_minutes": 20,
    "breaks_count": 1,
    "recovery_slots_count": 1
  },
  "weekly_objectives": ["Acquire basic Python syntax structures"]
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

def test_adaptive_rescheduling():
    scheduler = AdaptiveScheduler()
    missed = [
        ExecutionPlanItem(
            unit_id=uuid4(), mission_id=uuid4(), title="Missed focus session",
            estimated_duration=30, priority=0.8
        )
    ]
    slots = [{"start": "2026-08-01T15:00:00Z", "end": "2026-08-01T15:30:00Z", "window_name": "Afternoon"}]
    
    rescheduled = scheduler.reschedule_missed(missed, [], slots)
    assert len(rescheduled) == 1
    assert rescheduled[0].title == "Missed focus session"
    assert rescheduled[0].focus_window == "Afternoon"

@pytest.mark.asyncio
async def test_planner_agent_workflow(mock_gemini):
    from app.ai.runtime.container import container
    mem_manager = MockMemoryManager()
    container.behavior_memory = mem_manager
    container.identity_memory = mem_manager
    
    agent = PlannerAgent()
    
    state = LifeGPSState(
        event={"event_type": SystemEvent.USER_LOGIN, "payload": {}},
        session={"session_id": uuid4(), "client_platform": "windows"},
        user={"user_id": uuid4()}
    )
    
    context = ExecutionContext(
        workflow_id=uuid4(),
        execution_id=uuid4(),
        event=SystemEvent.USER_LOGIN,
        current_stage=WorkflowStage.PLANNING,
        current_agent="PlannerAgent"
    )
    
    result = await agent.execute(state, context)
    
    assert result.success
    assert result.explanation is not None
    assert "health_score" in result.explanation
    assert result.explanation["total_focused_minutes"] == 20
    assert len(state.daily_plan.tasks) == 1
