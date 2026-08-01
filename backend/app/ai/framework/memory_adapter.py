from typing import Any, Dict
from uuid import UUID
from app.ai.graph.memory_contracts import BaseMemoryManager

class MemoryAdapter:
    """Adapter bridging Agent domain operations to concrete MemoryManagers.
    
    Includes snapshot, rollback, and diffing features to support error recovery.
    """

    def __init__(self, manager: BaseMemoryManager):
        """Initializes the adapter.
        
        Args:
            manager: Target BaseMemoryManager implementation.
        """
        self.manager = manager

    async def load_memory(self, user_id: UUID) -> Dict[str, Any]:
        """Loads user memory state."""
        return await self.manager.load(user_id)

    async def save_memory(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Saves user memory state."""
        return await self.manager.save(user_id, data)

    async def update_memory(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Updates user memory state."""
        return await self.manager.update(user_id, data)

    async def archive_memory(self, user_id: UUID) -> bool:
        """Deletes user memory state, archiving current frames."""
        return await self.manager.delete(user_id)

    async def snapshot(self, user_id: UUID) -> Dict[str, Any]:
        """Captures a snapshot copy of current active memory.
        
        Args:
            user_id: User UUID.
            
        Returns:
            Dict[str, Any]: Copied memory state.
        """
        data = await self.load_memory(user_id)
        # Return deep copy of values
        import copy
        return copy.deepcopy(data)

    async def rollback(self, user_id: UUID, snapshot_data: Dict[str, Any]) -> bool:
        """Restores memory state back to snapshot properties.
        
        Args:
            user_id: User UUID.
            snapshot_data: The snapshot payload dictionary.
            
        Returns:
            bool: True if rollback succeeded.
        """
        await self.archive_memory(user_id)
        return await self.save_memory(user_id, snapshot_data)

    async def diff(self, user_id: UUID, compare_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compares current user memory with a comparison set.
        
        Args:
            user_id: User UUID.
            compare_data: Data set to check changes against.
            
        Returns:
            Dict[str, Any]: Changed keys and values.
        """
        current = await self.load_memory(user_id)
        changes = {}
        for k, v in current.items():
            if k not in compare_data or compare_data[k] != v:
                changes[k] = {"old": compare_data.get(k), "new": v}
        return changes
