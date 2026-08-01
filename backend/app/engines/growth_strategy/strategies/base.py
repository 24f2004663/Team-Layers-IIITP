from abc import ABC, abstractmethod
from app.engines.growth_strategy.schemas import StrategyProfile

class BaseStrategyPlugin(ABC):
    """Abstract interface defining the execution protocol for all Strategy Plugins."""

    @abstractmethod
    def get_name(self) -> str:
        """Returns name of strategy plugin."""
        pass

    @abstractmethod
    def build_profile(self, reasoning: str) -> StrategyProfile:
        """Builds profile variables conformed to this strategy's requirements.
        
        Args:
            reasoning: Contextual justification.
            
        Returns:
            StrategyProfile: Conformed settings.
        """
        pass
