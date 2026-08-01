from app.engines.evidence.engine import EvidenceEngine

def test_evidence_collection():
    engine = EvidenceEngine()
    ev = engine.collect_and_validate({
        "completed_missions": 2,
        "completed_units": 4,
        "session_duration": 120,
        "interruptions": 1,
        "mood": "Focused",
        "energy": "High",
        "errors": 1,
        "feedback_score": 0.95
    })
    
    assert ev.completed_missions_count == 2
    assert ev.session_duration_minutes == 120
    assert ev.user_feedback_score == 0.95
