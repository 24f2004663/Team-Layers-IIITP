from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.progress import Progress
from app.repositories.base import BaseRepository

class ProgressRepository(BaseRepository[Progress]):
    """Repository managing User Progress scores and quantitative growth histories."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(Progress, db_session)

    async def get_by_user_id(self, user_id: UUID) -> List[Progress]:
        """Retrieves all active progress logs matching target User UUID.
        
        Args:
            user_id: The UUID of the target user.
            
        Returns:
            List[Progress]: List of progress records.
        """
        result = await self.db.execute(
            select(Progress).where(Progress.user_id == user_id).where(Progress.deleted_at.is_(None))
        )
        return list(result.scalars().all())
