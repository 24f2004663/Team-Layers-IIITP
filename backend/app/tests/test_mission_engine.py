from app.engines.mission.engine import MissionEngine

def test_mission_generation_and_prioritization():
    engine = MissionEngine()
    
    missions = engine.generate_and_prioritize(
        decision_priority="Consistency",
        strategy_name="Tiny Habits",
        goal_graph=None,
        identity_alignment=0.80,
        overall_gap_score=0.35
    )
    
    assert len(missions) == 2
    assert missions[0].title == "Python Syntax Basics"
    assert missions[0].priority >= 0.90
    assert len(missions[0].execution_units) == 2
