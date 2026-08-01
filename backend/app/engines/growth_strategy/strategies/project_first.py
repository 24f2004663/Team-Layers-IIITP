from app.engines.growth_strategy.strategies.base import BaseStrategyPlugin
from app.engines.growth_strategy.schemas import StrategyProfile

class ProjectFirstStrategy(BaseStrategyPlugin):
    """Project-first strategy emphasizing direct practical execution context."""

    def get_name(self) -> str:
        return "Project First"

    def build_profile(self, reasoning: str) -> StrategyProfile:
        return StrategyProfile(
            objective="Accelerate career readiness by building functional portfolios.",
            reasoning=reasoning,
            success_metrics=["Completed portfolio repository", "PR reviews completed >= 2"],
            weekly_cadence=["Milestone planning Mon", "Code commits Wed/Fri", "Weekly demonstration Sunday"],
            adaptation_rules=["If blocked, convert goal decomposition tasks to micro coding milestones."]
        )
