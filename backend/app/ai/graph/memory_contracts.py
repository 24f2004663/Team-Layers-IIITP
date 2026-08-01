from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID

class BaseMemoryManager(ABC):
    """Base interface detailing mandatory memory operations for Life-GPS managers."""

    @abstractmethod
    async def load(self, user_id: UUID) -> Dict[str, Any]:
        """Loads memory state for a given user.
        
        Args:
            user_id: The UUID of the target user.
            
        Returns:
            A dictionary containing the retrieved memory payload.
        """
        raise NotImplementedError

    @abstractmethod
    async def save(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Saves memory state for a given user.
        
        Args:
            user_id: The UUID of the target user.
            data: The payload dictionary to persist.
            
        Returns:
            True if saving succeeded, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Partially updates active memory state.
        
        Args:
            user_id: The UUID of the target user.
            data: The partial update dictionary.
            
        Returns:
            True if updating succeeded, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Deletes active memory state.
        
        Args:
            user_id: The UUID of the target user.
            
        Returns:
            True if deletion succeeded, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def search(self, user_id: UUID, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries and searches memory elements matching context strings.
        
        Args:
            user_id: The UUID of the target user.
            query: Semantic query text.
            limit: Maximum count of matches.
            
        Returns:
            List of dictionaries matching search results.
        """
        raise NotImplementedError

    @abstractmethod
    async def summarize(self, user_id: UUID) -> str:
        """Synthesizes a short natural language summary of the active memory block.
        
        Args:
            user_id: The UUID of the target user.
            
        Returns:
            A string summary.
        """
        raise NotImplementedError


class IdentityMemoryManager(BaseMemoryManager, ABC):
    """Abstract interface managing user value profiles, personality traits, and archetypes."""


class BehaviorMemoryManager(BaseMemoryManager, ABC):
    """Abstract interface managing habit logs, energy levels, streaks, and cognitive traps."""


class ProgressMemoryManager(BaseMemoryManager, ABC):
    """Abstract interface managing historical task performance, milestone completion rates, and progress logs."""


class SemanticMemoryManager(BaseMemoryManager, ABC):
    """Abstract interface managing vector embeddings, journal entries, and semantic search indexes."""


class SessionMemoryManager(BaseMemoryManager, ABC):
    """Abstract interface managing transient dialogue loops, cache buffers, and chat message structures."""
