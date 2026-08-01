from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.identity import IdentityProfile
from app.repositories.base import BaseRepository

class IdentityRepository(BaseRepository[IdentityProfile]):
    """Repository managing User Identity profiles."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(IdentityProfile, db_session)

    async def get_by_user_id(self, user_id: UUID) -> Optional[IdentityProfile]:
        """Retrieves an identity profile matching target User UUID.
        
        Args:
            user_id: The UUID of the target user.
            
        Returns:
            Optional[IdentityProfile]: The found identity profile or None.
        """
        result = await self.db.execute(
            select(IdentityProfile).where(IdentityProfile.user_id == user_id).where(IdentityProfile.deleted_at.is_(None))
        )
        return result.scalars().first()
