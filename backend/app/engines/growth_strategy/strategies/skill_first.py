from app.engines.growth_strategy.strategies.base import BaseStrategyPlugin
from app.engines.growth_strategy.schemas import StrategyProfile

class SkillFirstStrategy(BaseStrategyPlugin):
    """Skill-first strategy building knowledge theory fundamentals."""

    def get_name(self) -> str:
        return "Skill First"

    def build_profile(self, reasoning: str) -> StrategyProfile:
        return StrategyProfile(
            objective="Establish theoretical competency before practical execution.",
            reasoning=reasoning,
            success_metrics=["Verified certifications acquisition", "Conceptual quiz score >= 80%"],
            weekly_cadence=["Reading sessions Tue/Thu", "Quiz validation Saturdays"],
            adaptation_rules=["If quiz fails, repeat roadmap milestone tasks with video lectures."]
        )
