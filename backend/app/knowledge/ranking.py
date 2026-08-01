from abc import ABC, abstractmethod
from typing import List
from app.knowledge.models import GrowthOpportunity

class GrowthOpportunityRanker(ABC):
    """Abstract interface defining scoring and ranking contracts for growth opportunities."""

    @abstractmethod
    async def score(self, opportunity: GrowthOpportunity) -> float:
        """Calculates a growth suitability score for a single opportunity.
        
        Args:
            opportunity: Target normalized growth opportunity.
            
        Returns:
            float: Scored rating value (e.g. 0.0 to 1.0).
        """
        raise NotImplementedError

    @abstractmethod
    async def rank(self, opportunities: List[GrowthOpportunity]) -> List[GrowthOpportunity]:
        """Ranks a list of growth opportunities in descending suitability order.
        
        Args:
            opportunities: Input list of opportunities.
            
        Returns:
            List[GrowthOpportunity]: Ranks sorted opportunities list.
        """
        raise NotImplementedError

    @abstractmethod
    async def explain(self, opportunity: GrowthOpportunity) -> str:
        """Generates a text explaining why this opportunity is suitable.
        
        Args:
            opportunity: Target normalized growth opportunity.
            
        Returns:
            str: Explanatory rationale text.
        """
        raise NotImplementedError
