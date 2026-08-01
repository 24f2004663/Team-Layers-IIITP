from app.engines.evidence.schemas import ExecutionEvidence
from app.engines.outcome.engine import OutcomeEngine

def test_outcome_analysis():
    engine = OutcomeEngine()
    ev = ExecutionEvidence(
        completed_missions_count=1,
        completed_execution_units=3,
        session_duration_minutes=90,
        interruptions_count=0,
        mood_value="Focused",
        energy_level="High",
        error_logs_count=0,
        user_feedback_score=0.90
    )
    
    out = engine.analyze(ev)
    assert out.mission_success_rate == 0.50
    assert out.learning_success_rate == 0.90
    assert out.identity_progress_score == 0.85
