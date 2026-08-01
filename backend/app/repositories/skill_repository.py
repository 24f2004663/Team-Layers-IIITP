from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.skill import Skill
from app.repositories.base import BaseRepository

class SkillRepository(BaseRepository[Skill]):
    """Repository managing User Skills."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(Skill, db_session)

    async def get_by_user_id(self, user_id: UUID) -> List[Skill]:
        """Retrieves all active skills matching target User UUID.
        
        Args:
            user_id: The UUID of the target user.
            
        Returns:
            List[Skill]: List of active skills.
        """
        result = await self.db.execute(
            select(Skill).where(Skill.user_id == user_id).where(Skill.deleted_at.is_(None))
        )
        return list(result.scalars().all())
