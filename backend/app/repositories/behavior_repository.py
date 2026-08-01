from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.behavior import BehaviorProfile
from app.repositories.base import BaseRepository

class BehaviorRepository(BaseRepository[BehaviorProfile]):
    """Repository managing User Behavior profiles."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(BehaviorProfile, db_session)

    async def get_by_user_id(self, user_id: UUID) -> Optional[BehaviorProfile]:
        """Retrieves a behavior profile matching target User UUID.
        
        Args:
            user_id: The UUID of the target user.
            
        Returns:
            Optional[BehaviorProfile]: The found behavior profile or None.
        """
        result = await self.db.execute(
            select(BehaviorProfile).where(BehaviorProfile.user_id == user_id).where(BehaviorProfile.deleted_at.is_(None))
        )
        return result.scalars().first()
