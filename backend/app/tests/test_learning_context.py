from app.engines.learning_context.engine import LearningContextEngine
from app.engines.mission.schemas import ExecutionUnit, Mission
from app.ai.agents.identity.schemas import IdentityProfile
from app.ai.agents.behavior.schemas import BehaviorProfile
from uuid import uuid4

def test_learning_context_compilation():
    engine = LearningContextEngine()
    
    m_id = uuid4()
    unit = ExecutionUnit(
        id=uuid4(), mission_id=m_id, title="Python loops basics",
        estimated_duration=45, required_energy="High", required_focus="High", priority=0.95
    )
    identity = IdentityProfile(
        identity_summary="Seed Profile", career_goal="AI Architect", mission="Coding",
        core_values=["Craftsmanship"], interests=["AI"], strengths=["Math"], weaknesses=["Syntax"], confidence_score=0.9
    )
    behavior = BehaviorProfile(
        learning_style="Project-Based", focus_style="Spurt", attention_span_minutes=30,
        productive_hours=[9], preferred_session_length=45, procrastination_level="Low",
        consistency_score=0.8, adaptability_score=0.7, motivation_level="Medium",
        energy_pattern="Morning Peak", stress_pattern="Stable", confidence_score=0.9
    )
    mission = Mission(
        title="Python Basics", objective="Master syntax structures", description="Read code",
        supporting_gap="Syntax gap", supporting_strategy="Tiny Habits", estimated_duration=60,
        difficulty="Easy", priority=0.9, deadline="2026-08-01", energy_requirement="Medium",
        focus_requirement="Medium", confidence=0.9, reasoning="Pre-req syntax"
    )
    
    ctx = engine.generate_context(unit, identity, behavior, mission)
    assert ctx.available_time == 45
    assert ctx.preferred_learning_style == "Project-Based"
