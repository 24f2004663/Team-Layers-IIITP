from abc import ABC, abstractmethod
from typing import List, Optional
from app.knowledge.models import GrowthOpportunity, OpportunityType
from app.knowledge.context import KnowledgeQuery

class KnowledgeProvider(ABC):
    """Abstract interface defining the requirements for external growth resource providers."""

    @abstractmethod
    async def search(self, query: KnowledgeQuery) -> List[GrowthOpportunity]:
        """Queries the provider to retrieve growth opportunities matching query context.
        
        Args:
            query: The standardized query context.
            
        Returns:
            List[GrowthOpportunity]: Retrieved normalized opportunities.
        """
        raise NotImplementedError

    @abstractmethod
    async def fetch(self, opportunity_id: str) -> Optional[GrowthOpportunity]:
        """Retrieves a single growth opportunity by its provider-specific ID.
        
        Args:
            opportunity_id: Provider specific unique identifier.
            
        Returns:
            Optional[GrowthOpportunity]: The found opportunity details or None.
        """
        raise NotImplementedError

    @abstractmethod
    async def health(self) -> bool:
        """Evaluates health and latency of the provider integration.
        
        Returns:
            bool: True if connection is alive, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def supports(self, opportunity_type: OpportunityType) -> bool:
        """Evaluates whether the provider supports searching for a given type.
        
        Args:
            opportunity_type: Target category enum value.
            
        Returns:
            bool: True if supported, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def get_provider_name(self) -> str:
        """Returns the unique name identifier of the provider.
        
        Returns:
            str: Provider name (e.g. 'YouTube').
        """
        raise NotImplementedError
