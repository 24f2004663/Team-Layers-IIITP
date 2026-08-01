from typing import Any, Dict, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.graph.memory_contracts import BehaviorMemoryManager
from app.repositories.behavior_repository import BehaviorRepository
from app.infrastructure.logging.logger import logger

class SQLBehaviorMemoryManager(BehaviorMemoryManager):
    """Memory manager bridge for Behavior profiles persistence using SQLAlchemy repositories."""

    def __init__(self, db: AsyncSession):
        """Initializes the manager.
        
        Args:
            db: Active database AsyncSession.
        """
        self.repo = BehaviorRepository(db)

    async def load(self, user_id: UUID) -> Dict[str, Any]:
        """Loads behavior profile memory for user.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            Dict[str, Any]: Profile details.
        """
        profile = await self.repo.get_by_user_id(user_id)
        if not profile:
            return {}
        return {
            "habits": profile.habits,
            "cognitive_patterns": profile.cognitive_patterns,
            "energy_levels": profile.energy_levels,
        }

    async def save(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Saves behavior profile memory.
        
        Args:
            user_id: Target user UUID.
            data: Data payload to save.
            
        Returns:
            bool: True if success, False otherwise.
        """
        try:
            profile = await self.repo.get_by_user_id(user_id)
            if profile:
                await self.repo.update(profile.id, data)
            else:
                db_data = {"user_id": user_id, **data}
                await self.repo.create(db_data)
            return True
        except Exception as e:
            logger.error("BehaviorMemoryManager save failed", error=str(e), user_id=str(user_id))
            return False

    async def update(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Updates active behavior profile memory.
        
        Args:
            user_id: Target user UUID.
            data: Update payload.
            
        Returns:
            bool: True if success, False otherwise.
        """
        return await self.save(user_id, data)

    async def delete(self, user_id: UUID) -> bool:
        """Soft-deletes the target behavior profile memory.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            bool: True if success, False otherwise.
        """
        profile = await self.repo.get_by_user_id(user_id)
        if not profile:
            return False
        return await self.repo.delete(profile.id, soft=True)

    async def search(self, user_id: UUID, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries active habit logs matching string keys.
        
        Args:
            user_id: Target user UUID.
            query: String query to find.
            limit: Maximum count.
            
        Returns:
            List[Dict[str, Any]]: Matching elements.
        """
        profile = await self.load(user_id)
        if not profile:
            return []
        
        matches = []
        q = query.lower()
        for habit_key, habit_data in profile.get("habits", {}).items():
            if q in habit_key.lower():
                matches.append({"habit": habit_key, "data": habit_data})
        return matches[:limit]

    async def summarize(self, user_id: UUID) -> str:
        """Summarizes behavior patterns.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            str: Summary.
        """
        profile = await self.load(user_id)
        if not profile:
            return "No behavior profile established."
        return f"User habits currently include {len(profile.get('habits', {}))} items, with {len(profile.get('cognitive_patterns', []))} tracked patterns."
