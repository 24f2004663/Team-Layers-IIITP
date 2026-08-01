import asyncio
from typing import List, Set
from app.knowledge.models import GrowthOpportunity
from app.knowledge.context import KnowledgeQuery
from app.knowledge.registry import ProviderRegistry
from app.infrastructure.logging.logger import logger

class KnowledgeAggregator:
    """Aggregates and merges growth opportunities discovered by matching registered providers."""

    def __init__(self, registry: ProviderRegistry):
        """Initializes the aggregator.
        
        Args:
            registry: The ProviderRegistry instance.
        """
        self.registry = registry

    async def aggregate(self, query: KnowledgeQuery) -> List[GrowthOpportunity]:
        """Queries matching providers concurrently and returns normalized merged opportunities.
        
        Args:
            query: The parameters specifying target skills and formats.
            
        Returns:
            List[GrowthOpportunity]: De-duplicated list of growth opportunities.
        """
        # Determine target providers based on query preferred types
        target_providers = set()
        
        if query.preferred_types:
            for opt_type in query.preferred_types:
                providers = self.registry.find_by_type(opt_type)
                target_providers.update(providers)
        else:
            # Fallback to all registered providers if no preferred types specified
            for name in self.registry.list_providers():
                target_providers.add(self.registry.get_provider(name))
                
        # Filter out excluded sources
        active_providers = [
            prov for prov in target_providers
            if prov.get_provider_name() not in query.excluded_sources
        ]
        
        if not active_providers:
            logger.warning("No active knowledge providers match search constraints.")
            return []
            
        # Run search across all matched providers concurrently
        logger.info(f"Querying {len(active_providers)} active knowledge providers concurrently...")
        tasks = [prov.search(query) for prov in active_providers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        merged_list: List[GrowthOpportunity] = []
        seen_urls: Set[str] = set()
        
        for idx, res in enumerate(results):
            provider_name = active_providers[idx].get_provider_name()
            if isinstance(res, Exception):
                logger.error("Provider query execution failed", provider=provider_name, error=str(res))
                continue
                
            for opportunity in res:
                # Deduplicate by destination URL
                if opportunity.url in seen_urls:
                    continue
                seen_urls.add(opportunity.url)
                merged_list.append(opportunity)
                
        logger.info(f"Aggregation complete. Retrieved {len(merged_list)} distinct growth opportunities.")
        return merged_list
