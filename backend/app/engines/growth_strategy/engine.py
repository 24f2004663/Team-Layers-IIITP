from typing import Dict
from app.engines.growth_strategy.schemas import GrowthStrategyOutput
from app.engines.growth_strategy.strategies.tiny_habits import TinyHabitsStrategy
from app.engines.growth_strategy.strategies.deep_work import DeepWorkStrategy
from app.engines.growth_strategy.strategies.project_first import ProjectFirstStrategy
from app.engines.growth_strategy.strategies.skill_first import SkillFirstStrategy

class GrowthStrategyEngine:
    """The Growth Strategy Engine dynamically matches priority focus targets to plugin executors."""

    def __init__(self):
        # Register strategy plugins
        self.plugins = {
            "Tiny Habits": TinyHabitsStrategy(),
            "Deep Work": DeepWorkStrategy(),
            "Project First": ProjectFirstStrategy(),
            "Skill First": SkillFirstStrategy()
        }

    def resolve_strategy(self, strategy_choice: str, reasoning: str) -> GrowthStrategyOutput:
        """Loads matched strategy plugin properties.
        
        Args:
            strategy_choice: Matched strategy name.
            reasoning: Justification statement.
            
        Returns:
            GrowthStrategyOutput: Strategy configuration details.
        """
        # Default fallback to Tiny Habits if strategy plugin isn't direct
        plugin = self.plugins.get(strategy_choice, self.plugins["Tiny Habits"])
        
        profile = plugin.build_profile(reasoning)
        return GrowthStrategyOutput(
            strategy_name=plugin.get_name(),
            profile=profile
        )
