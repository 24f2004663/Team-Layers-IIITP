from app.engines.growth_strategy.strategies.base import BaseStrategyPlugin
from app.engines.growth_strategy.schemas import StrategyProfile

class TinyHabitsStrategy(BaseStrategyPlugin):
    """Encapsulates consistency building via atomic habits loops."""

    def get_name(self) -> str:
        return "Tiny Habits"

    def build_profile(self, reasoning: str) -> StrategyProfile:
        return StrategyProfile(
            objective="Build micro-streaks through small, incremental habits.",
            reasoning=reasoning,
            success_metrics=["Streak completion rate >= 85%", "Consistency score >= 0.8"],
            weekly_cadence=["5 minutes daily study block", "Weekend alignment review"],
            adaptation_rules=["If streak fails twice, reduce block size to 2 minutes."]
        )
