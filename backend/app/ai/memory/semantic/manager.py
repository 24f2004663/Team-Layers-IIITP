from typing import Any, Dict, List
from uuid import UUID
from app.ai.graph.memory_contracts import SemanticMemoryManager
from app.infrastructure.logging.logger import logger

class MockSemanticMemoryManager(SemanticMemoryManager):
    """Placeholder Memory manager for pgvector-based semantic search embeddings."""

    def __init__(self):
        """Initializes the mock storage."""
        self._store: Dict[UUID, List[Dict[str, Any]]] = {}

    async def load(self, user_id: UUID) -> Dict[str, Any]:
        """Loads semantic nodes.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            Dict[str, Any]: Semantic nodes list.
        """
        nodes = self._store.get(user_id, [])
        return {"nodes": nodes}

    async def save(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Saves a semantic text chunk node.
        
        Args:
            user_id: Target user UUID.
            data: Content payload.
            
        Returns:
            bool: True if success.
        """
        if user_id not in self._store:
            self._store[user_id] = []
        self._store[user_id].append(data)
        logger.info("SemanticMemoryManager saved vector chunk placeholder", user_id=str(user_id), payload=data)
        return True

    async def update(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Updates active semantic node memory.
        
        Args:
            user_id: Target user UUID.
            data: Update payload.
            
        Returns:
            bool: True.
        """
        return await self.save(user_id, data)

    async def delete(self, user_id: UUID) -> bool:
        """Cleans user semantic store.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            bool: True.
        """
        if user_id in self._store:
            del self._store[user_id]
        return True

    async def search(self, user_id: UUID, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries and searches active semantic nodes.
        
        Args:
            user_id: Target user UUID.
            query: Query text.
            limit: Limit.
            
        Returns:
            List[Dict[str, Any]]: Matches.
        """
        nodes = self._store.get(user_id, [])
        matches = []
        q = query.lower()
        for node in nodes:
            content = node.get("content", "")
            if q in content.lower():
                matches.append(node)
        return matches[:limit]

    async def summarize(self, user_id: UUID) -> str:
        """Summarizes semantic profile.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            str: Summary.
        """
        nodes = self._store.get(user_id, [])
        return f"Semantic archive contains {len(nodes)} indexed vector placeholders."
