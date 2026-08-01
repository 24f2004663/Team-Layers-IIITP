from app.engines.growth_strategy.strategies.base import BaseStrategyPlugin
from app.engines.growth_strategy.schemas import StrategyProfile

class DeepWorkStrategy(BaseStrategyPlugin):
    """Deep Work strategy prioritizing high focus span blocks."""

    def get_name(self) -> str:
        return "Deep Work"

    def build_profile(self, reasoning: str) -> StrategyProfile:
        return StrategyProfile(
            objective="Maximize uninterrupted concentration blocks to acquire complex skills.",
            reasoning=reasoning,
            success_metrics=["Attention span >= 45 mins", "Deep focus block counts >= 4/week"],
            weekly_cadence=["90 min focus sessions on Mon/Wed/Fri", "Weekly cognitive patterns analysis"],
            adaptation_rules=["If interruptions > 3, enable full focus mode settings."]
        )
