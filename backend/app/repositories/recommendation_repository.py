from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.recommendation import Recommendation
from app.repositories.base import BaseRepository

class RecommendationRepository(BaseRepository[Recommendation]):
    """Repository managing User Recommendations and references."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(Recommendation, db_session)

    async def get_by_user_id(self, user_id: UUID) -> List[Recommendation]:
        """Retrieves all active recommendations matching target User UUID.
        
        Args:
            user_id: The UUID of the target user.
            
        Returns:
            List[Recommendation]: List of recommendations.
        """
        result = await self.db.execute(
            select(Recommendation).where(Recommendation.user_id == user_id).where(Recommendation.deleted_at.is_(None))
        )
        return list(result.scalars().all())
