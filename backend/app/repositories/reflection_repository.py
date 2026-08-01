from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.reflection import Reflection
from app.repositories.base import BaseRepository

class ReflectionRepository(BaseRepository[Reflection]):
    """Repository managing User Reflections and cognitive insight logs."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(Reflection, db_session)

    async def get_by_user_id(self, user_id: UUID) -> List[Reflection]:
        """Retrieves all active reflection records matching target User UUID.
        
        Args:
            user_id: The UUID of the target user.
            
        Returns:
            List[Reflection]: List of reflections.
        """
        result = await self.db.execute(
            select(Reflection).where(Reflection.user_id == user_id).where(Reflection.deleted_at.is_(None))
        )
        return list(result.scalars().all())
