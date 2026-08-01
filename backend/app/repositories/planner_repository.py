from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.daily_plan import DailyPlan
from app.repositories.base import BaseRepository

class PlannerRepository(BaseRepository[DailyPlan]):
    """Repository managing User Daily plans and schedule metadata."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(DailyPlan, db_session)

    async def get_by_date(self, user_id: UUID, target_date: datetime) -> Optional[DailyPlan]:
        """Retrieves a daily plan for a specific date and user.
        
        Args:
            user_id: The UUID of the target user.
            target_date: Target date to retrieve.
            
        Returns:
            Optional[DailyPlan]: The found daily plan or None.
        """
        # Truncate time for pure date matching in DB or simple equivalence filter
        result = await self.db.execute(
            select(DailyPlan)
            .where(DailyPlan.user_id == user_id)
            .where(DailyPlan.date == target_date)
            .where(DailyPlan.deleted_at.is_(None))
        )
        return result.scalars().first()
