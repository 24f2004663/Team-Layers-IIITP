import pytest
from uuid import uuid4
from unittest.mock import MagicMock, AsyncMock

from app.ai.graph.events import SystemEvent
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.ai.graph.workflow import WorkflowStage
from app.ai.agents.curator.agent import CuratorAgent
from app.ai.agents.curator.experience_composer import ExperienceComposer
from app.ai.framework.messages import AIResponse
from app.ai.llm.factory import llm_factory

class MockMemoryManager:
    def __init__(self):
        self.db = {}

    async def load(self, user_id):
        return self.db.get(user_id, {"experience_bundles_history": [], "experiences_timeline": []})

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
  "bundle": {
    "primary_video": "https://youtube.com/py-var",
    "official_documentation": "https://scikit-learn.org",
    "practice_exercise": "https://practice.com/py-loops",
    "mini_project": "https://github.com/project/ml-basic",
    "github_repository": "https://github.com/project/reference-code",
    "quiz": "https://quiz.com/py-var",
    "optional_reading": "Optional article on Python optimization",
    "reflection_question": "How does memory lookup compare between dictionaries and lists?",
    "estimated_completion_time_minutes": 45,
    "expected_skill_gains": [
      {
        "skill_name": "Python",
        "gain_percentage": 0.08
      },
      {
        "skill_name": "REST APIs",
        "gain_percentage": 0.15
      },
      {
        "skill_name": "Problem Solving",
        "gain_percentage": 0.06
      }
    ],
    "resource_diversity_score": 0.85,
    "path_order_sequence": [
      "1. Video: Understand core concepts",
      "2. Documentation: Review syntax and APIs",
      "3. Practice: Complete exercises loops basics",
      "4. Mini Project: Build mock application",
      "5. Reflection: Self review"
    ],
    "standard_option": "Standard: Follow full 5-step pathway",
    "fast_track_option": "Fast Track: Skip video, do documentation & practice",
    "deep_dive_option": "Deep Dive: Build full project and read optional papers",
    "confidence": 0.90,
    "quality_score": {
      "relevance": 0.92,
      "diversity": 0.85,
      "time_efficiency": 0.88,
      "skill_coverage": 0.90,
      "historical_success": 0.85,
      "confidence": 0.95
    },
    "explanation": {
      "why_this_resource": "Top ranked high-quality video matched to style",
      "why_now": "Aligned with morning focus slot availability",
      "how_it_supports_mission": "Prerequisite coding basics",
      "which_skill_gap_it_closes": "Loops syntax gap",
      "expected_learning_outcome": "Understand list structures",
      "confidence": 0.95,
      "alternative_option": "Fast Track: Documentation & Practice only"
    }
  },
  "candidates_ranked": [
    {
      "resource_name": "Learn Python Variables video",
      "resource_type": "Video",
      "url": "https://youtube.com/py-var",
      "score": 0.95,
      "rank": 1,
      "quality_score": 0.95,
      "opportunity_readiness": {
        "readiness_percentage": 0.82,
        "missing_skills": ["Docker"],
        "preparation_time_hours": 12.0
      }
    }
  ]
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

def test_experience_composer():
    composer = ExperienceComposer()
    bundle = composer.compose_and_optimize({"primary_video": "https://youtube.com/py-var"})
    
    assert bundle.resource_diversity_score == 0.85
    assert len(bundle.path_order_sequence) == 5
    assert bundle.expected_skill_gains[0].skill_name == "Python"
    assert bundle.expected_skill_gains[0].gain_percentage == 0.08

@pytest.mark.asyncio
async def test_curator_agent_workflow(mock_gemini):
    from app.ai.runtime.container import container
    mem_manager = MockMemoryManager()
    container.behavior_memory = mem_manager
    container.identity_memory = mem_manager
    
    agent = CuratorAgent()
    
    state = LifeGPSState(
        event={"event_type": SystemEvent.TASK_COMPLETED, "payload": {}},
        session={"session_id": uuid4(), "client_platform": "windows"},
        user={"user_id": uuid4()}
    )
    
    context = ExecutionContext(
        workflow_id=uuid4(),
        execution_id=uuid4(),
        event=SystemEvent.TASK_COMPLETED,
        current_stage=WorkflowStage.CURATION,
        current_agent="CuratorAgent"
    )
    
    result = await agent.execute(state, context)
    
    assert result.success
    assert result.explanation is not None
    assert "why_this_resource" in result.explanation
    assert len(result.explanation["skills_gain"]) == 3
