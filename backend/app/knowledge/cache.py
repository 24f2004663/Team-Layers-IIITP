from abc import ABC, abstractmethod
from typing import List, Optional
from app.knowledge.models import GrowthOpportunity

class KnowledgeCache(ABC):
    """Abstract interface defining transient cache storage contracts for Growth Opportunities."""

    @abstractmethod
    async def get(self, key: str) -> Optional[List[GrowthOpportunity]]:
        """Retrieves cached opportunities matching target lookup key.
        
        Args:
            key: Cached key.
            
        Returns:
            Optional[List[GrowthOpportunity]]: Cached results list or None if miss.
        """
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: List[GrowthOpportunity], ttl: int = 3600) -> bool:
        """Caches list of opportunities matching target lookup key.
        
        Args:
            key: Target cache lookup key.
            value: Opportunities list to cache.
            ttl: Time to live in seconds.
            
        Returns:
            bool: True if cache updated successfully, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def invalidate(self, key: str) -> bool:
        """Invalidates cache entries matching target key.
        
        Args:
            key: Cached key to clear.
            
        Returns:
            bool: True if invalidated, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> bool:
        """Flushes all stored entries from the cache.
        
        Returns:
            bool: True if clear operations succeeded.
        """
        raise NotImplementedError
