from typing import Any, Dict, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.graph.memory_contracts import IdentityMemoryManager
from app.repositories.identity_repository import IdentityRepository
from app.infrastructure.logging.logger import logger

class SQLIdentityMemoryManager(IdentityMemoryManager):
    """Memory manager bridge for Identity profiles persistence using SQLAlchemy repositories."""

    def __init__(self, db: AsyncSession):
        """Initializes the manager.
        
        Args:
            db: Active database AsyncSession.
        """
        self.repo = IdentityRepository(db)

    async def load(self, user_id: UUID) -> Dict[str, Any]:
        """Loads identity profile memory for user.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            Dict[str, Any]: Profile details dictionary.
        """
        profile = await self.repo.get_by_user_id(user_id)
        if not profile:
            return {}
        return {
            "archetype": profile.archetype,
            "core_values": profile.core_values,
            "strengths": profile.strengths,
            "weaknesses": profile.weaknesses,
        }

    async def save(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Saves identity profile memory.
        
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
            logger.error("IdentityMemoryManager save failed", error=str(e), user_id=str(user_id))
            return False

    async def update(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Updates active identity profile memory.
        
        Args:
            user_id: Target user UUID.
            data: Update payload.
            
        Returns:
            bool: True if success, False otherwise.
        """
        return await self.save(user_id, data)

    async def delete(self, user_id: UUID) -> bool:
        """Soft-deletes the target identity profile memory.
        
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
        """Performs simple text query match on the archetype and strengths.
        
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
        if q in profile.get("archetype", "").lower():
            matches.append({"field": "archetype", "value": profile["archetype"]})
        for strength in profile.get("strengths", []):
            if q in strength.lower():
                matches.append({"field": "strengths", "value": strength})
                
        return matches[:limit]

    async def summarize(self, user_id: UUID) -> str:
        """Summarizes identity details in text format.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            str: Natural language summary of the user identity.
        """
        profile = await self.load(user_id)
        if not profile:
            return "No identity profile established."
        return f"User is classified as a {profile.get('archetype', 'Unknown')} archetype. Core strengths include: {', '.join(profile.get('strengths', []))}."
