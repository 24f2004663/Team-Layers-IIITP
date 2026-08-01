from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.goal import Goal
from app.repositories.base import BaseRepository

class GoalRepository(BaseRepository[Goal]):
    """Repository managing User Goals."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(Goal, db_session)

    async def get_by_user_id(self, user_id: UUID) -> List[Goal]:
        """Retrieves all active goals matching target User UUID.
        
        Args:
            user_id: The UUID of the target user.
            
        Returns:
            List[Goal]: List of active goals.
        """
        result = await self.db.execute(
            select(Goal).where(Goal.user_id == user_id).where(Goal.deleted_at.is_(None))
        )
        return list(result.scalars().all())
