from typing import Any, Dict, List
from uuid import UUID
from app.ai.graph.memory_contracts import SessionMemoryManager
from app.infrastructure.logging.logger import logger

class MockSessionMemoryManager(SessionMemoryManager):
    """Placeholder Memory manager for Redis-based transient session cache logs."""

    def __init__(self):
        """Initializes the mock memory cache."""
        self._cache: Dict[UUID, Dict[str, Any]] = {}

    async def load(self, user_id: UUID) -> Dict[str, Any]:
        """Loads transient cache details.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            Dict[str, Any]: Cached session payload.
        """
        return self._cache.get(user_id, {})

    async def save(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Saves session cache transient logs.
        
        Args:
            user_id: Target user UUID.
            data: Data payload to save.
            
        Returns:
            bool: True.
        """
        self._cache[user_id] = data
        logger.info("SessionMemoryManager cached payload in Redis placeholder", user_id=str(user_id), payload=data)
        return True

    async def update(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Updates active session memory.
        
        Args:
            user_id: Target user UUID.
            data: Update payload.
            
        Returns:
            bool: True.
        """
        current = await self.load(user_id)
        current.update(data)
        return await self.save(user_id, current)

    async def delete(self, user_id: UUID) -> bool:
        """Flushes user session cache.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            bool: True.
        """
        if user_id in self._cache:
            del self._cache[user_id]
        return True

    async def search(self, user_id: UUID, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries and searches active transient cache logs.
        
        Args:
            user_id: Target user UUID.
            query: Query string.
            limit: Limit.
            
        Returns:
            List[Dict[str, Any]]: Matches.
        """
        # Session search is not typically indexed, returning empty list
        return []

    async def summarize(self, user_id: UUID) -> str:
        """Summarizes session profile.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            str: Summary.
        """
        data = await self.load(user_id)
        return f"Transient session cache size: {len(data)} active parameters."
