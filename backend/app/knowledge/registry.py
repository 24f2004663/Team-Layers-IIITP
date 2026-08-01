from typing import Dict, List
from app.knowledge.providers.base import KnowledgeProvider
from app.knowledge.models import OpportunityType
from app.infrastructure.logging.logger import logger

class ProviderRegistry:
    """Registry managing active KnowledgeProviders at runtime."""

    def __init__(self):
        self._providers: Dict[str, KnowledgeProvider] = {}

    def register(self, provider: KnowledgeProvider) -> None:
        """Registers a provider into the active registry pool.
        
        Args:
            provider: Concrete KnowledgeProvider object.
        """
        name = provider.get_provider_name()
        self._providers[name] = provider
        logger.info("Successfully registered knowledge provider", provider_name=name)

    def unregister(self, provider_name: str) -> None:
        """Removes a provider from the active registry pool.
        
        Args:
            provider_name: The name identifier of the provider.
        """
        if provider_name in self._providers:
            del self._providers[provider_name]
            logger.info("Unregistered knowledge provider", provider_name=provider_name)

    def list_providers(self) -> List[str]:
        """Lists names of all registered providers.
        
        Returns:
            List[str]: Provider name list.
        """
        return list(self._providers.keys())

    def get_provider(self, provider_name: str) -> KnowledgeProvider:
        """Retrieves a registered provider object by name.
        
        Args:
            provider_name: Name of the provider.
            
        Returns:
            KnowledgeProvider: Registered provider instance.
            
        Raises:
            KeyError: If provider not found.
        """
        if provider_name not in self._providers:
            raise KeyError(f"Provider '{provider_name}' not registered.")
        return self._providers[provider_name]

    def find_by_type(self, opportunity_type: OpportunityType) -> List[KnowledgeProvider]:
        """Resolves all providers supporting a given opportunity classification type.
        
        Args:
            opportunity_type: Opportunity format classification.
            
        Returns:
            List[KnowledgeProvider]: Supporting providers list.
        """
        return [
            prov for prov in self._providers.values()
            if prov.supports(opportunity_type)
        ]
