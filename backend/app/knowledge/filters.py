from abc import ABC, abstractmethod
from typing import List
from app.knowledge.models import GrowthOpportunity
from app.knowledge.context import KnowledgeQuery

class BaseOpportunityFilter(ABC):
    """Abstract interface defining the requirements for opportunity filtering components."""

    @abstractmethod
    def filter(self, opportunities: List[GrowthOpportunity], query: KnowledgeQuery) -> List[GrowthOpportunity]:
        """Applies filter constraints on a list of growth opportunities.
        
        Args:
            opportunities: Input list of opportunities.
            query: Active query parameters providing filter keys.
            
        Returns:
            List[GrowthOpportunity]: Filtered opportunities list.
        """
        raise NotImplementedError


class DifficultyFilter(BaseOpportunityFilter, ABC):
    """Abstract filter verifying that the opportunity difficulty matches user target limits."""


class TimeFilter(BaseOpportunityFilter, ABC):
    """Abstract filter verifying that the estimated duration is within available time slots."""


class LearningStyleFilter(BaseOpportunityFilter, ABC):
    """Abstract filter aligning opportunity formats with user learning preferences."""


class LanguageFilter(BaseOpportunityFilter, ABC):
    """Abstract filter matching opportunity language constraints."""


class SkillFilter(BaseOpportunityFilter, ABC):
    """Abstract filter matching target skills requested in the query."""


class CostFilter(BaseOpportunityFilter, ABC):
    """Abstract filter ensuring cost values are within user budget limits."""
