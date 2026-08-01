import pytest
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, AsyncMock

from app.ai.graph.events import SystemEvent
from app.ai.graph.state import LifeGPSState
from app.ai.runtime.context import ExecutionContext
from app.ai.graph.workflow import WorkflowStage
from app.ai.agents.behavior.agent import BehaviorAgent
from app.ai.agents.behavior.schemas import BehaviorProfile, BehaviorObservation, PatternStability
from app.ai.agents.behavior.metrics import GapAnalyzer, ConfidenceDecay
from app.ai.agents.behavior.evidence_engine import BehaviorEvidenceEngine
from app.ai.agents.behavior.pattern_analyzer import PatternAnalyzer
from app.ai.agents.behavior.drift_detector import BehaviorDriftDetector
from app.ai.agents.identity.schemas import IdentityProfile
from app.ai.framework.messages import AIResponse
from app.ai.llm.factory import llm_factory
from app.ai.framework.errors import ValidationError

class MockBehaviorMemoryManager:
    def __init__(self):
        self.db = {}

    async def load(self, user_id):
        return self.db.get(user_id, {"observations": [], "evidence": [], "patterns": [], "timeline": []})

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
  "learning_style": "Visual",
  "focus_style": "Deep Work",
  "attention_span_minutes": 45,
  "productive_hours": [9, 10, 14, 15],
  "preferred_session_length": 45,
  "procrastination_level": "Low",
  "consistency_score": 0.85,
  "adaptability_score": 0.80,
  "motivation_level": "High",
  "energy_pattern": "Morning Peak",
  "stress_pattern": "Normal",
  "confidence_score": 0.90
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

def test_observation_extraction():
    agent = BehaviorAgent()
    payload = {"task_name": "Read AI chapter", "duration_minutes": 50, "source": "Scheduler"}
    obs = agent.extractor.extract_observation(SystemEvent.TASK_COMPLETED, payload)
    
    assert obs.event_type == "TASK_COMPLETED"
    assert "Read AI chapter" in obs.description
    assert obs.duration == 50

def test_evidence_engine_synthesis():
    engine = BehaviorEvidenceEngine()
    obs_list = [
        BehaviorObservation(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc).replace(hour=21),
            event_type="TASK_COMPLETED",
            source="Scheduler",
            description="Completed late study session",
            duration=40
        )
    ]
    evidences = engine.generate_evidence(obs_list)
    assert len(evidences) >= 1
    assert any("Night Learner" in ev.hypothesis for ev in evidences)

def test_pattern_stability_discovery():
    engine = BehaviorEvidenceEngine()
    analyzer = PatternAnalyzer()
    
    obs_list = [
        BehaviorObservation(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc).replace(hour=22),
            event_type="TASK_COMPLETED",
            source="Scheduler",
            description="Completed late session 1",
            duration=40
        ),
        BehaviorObservation(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc).replace(hour=23),
            event_type="TASK_COMPLETED",
            source="Scheduler",
            description="Completed late session 2",
            duration=45
        ),
        BehaviorObservation(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc).replace(hour=21),
            event_type="TASK_COMPLETED",
            source="Scheduler",
            description="Completed late session 3",
            duration=35
        )
    ]
    
    evidences = engine.generate_evidence(obs_list)
    patterns = analyzer.analyze_patterns(evidences)
    
    assert len(patterns) >= 1
    # High support weight maps trend to STABLE or EMERGING
    assert patterns[0].trend in [PatternStability.STABLE, PatternStability.EMERGING]

def test_drift_warnings():
    detector = BehaviorDriftDetector()
    current = BehaviorProfile(
        learning_style="Visual",
        focus_style="Deep Work",
        attention_span_minutes=45,
        productive_hours=[9, 10],
        preferred_session_length=45,
        procrastination_level="Low",
        consistency_score=0.60,  # Dropped from 0.80 baseline
        adaptability_score=0.80,
        motivation_level="High",
        energy_pattern="Morning Peak",
        stress_pattern="Normal",
        confidence_score=0.90
    )
    baseline = {"consistency_score": 0.80, "attention_span_minutes": 45}
    warnings = detector.detect_drift(current, baseline)
    assert len(warnings) == 1
    assert warnings[0].metric == "consistency_score"

def test_three_dimensional_decay():
    decay = ConfidenceDecay(decay_rate_per_day=0.1)
    
    # Check recency and frequency components
    val1 = decay.calculate_decayed_confidence(1.0, datetime.now(timezone.utc), datetime.now(timezone.utc), frequency=1)
    val2 = decay.calculate_decayed_confidence(1.0, datetime.now(timezone.utc) - timedelta(days=5), datetime.now(timezone.utc), frequency=1)
    
    assert val2 < val1

def test_gap_analysis():
    calc = GapAnalyzer()
    
    identity = IdentityProfile(
        identity_summary="Aspiring AI Engineer",
        career_goal="Senior Engineer",
        mission="Build robust systems",
        core_values=["Growth"],
        interests=["Python"],
        strengths=["Logic"],
        weaknesses=[],
        learning_style="Visual",
        motivation_level="High",
        confidence_score=0.9
    )
    
    behavior = BehaviorProfile(
        learning_style="Visual",
        focus_style="Deep Work",
        attention_span_minutes=45,
        productive_hours=[9, 10],
        preferred_session_length=45,
        procrastination_level="Low",
        consistency_score=0.90,
        adaptability_score=0.80,
        motivation_level="High",
        energy_pattern="Morning Peak",
        stress_pattern="Normal",
        confidence_score=0.90
    )
    
    alignment, insights = calc.analyze_gaps(identity, behavior)
    assert alignment.alignment_score >= 0.80
    assert len(insights) >= 1
    assert insights[0].title == "Excellent Consistency"

@pytest.mark.asyncio
async def test_behavior_agent_workflow(mock_gemini):
    from app.ai.runtime.container import container
    mem_manager = MockBehaviorMemoryManager()
    container.behavior_memory = mem_manager
    
    agent = BehaviorAgent()
    
    state = LifeGPSState(
        event={
            "event_type": SystemEvent.TASK_COMPLETED,
            "payload": {
                "task_name": "Implement vector search",
                "duration_minutes": 60,
                "source": "PlannerWidget"
            }
        },
        session={"session_id": uuid4(), "client_platform": "windows"},
        user={"user_id": uuid4()}
    )
    
    context = ExecutionContext(
        workflow_id=uuid4(),
        execution_id=uuid4(),
        event=SystemEvent.TASK_COMPLETED,
        current_stage=WorkflowStage.ANALYSIS,
        current_agent="BehaviorAgent"
    )
    
    result = await agent.execute(state, context)
    
    assert result.success
    assert result.explanation is not None
    assert "agent_output" in result.explanation
    
    saved_data = mem_manager.db[state.user.user_id]
    assert len(saved_data["observations"]) == 1
    assert len(saved_data["evidence"]) >= 1
