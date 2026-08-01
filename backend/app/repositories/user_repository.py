from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """Repository managing User accounts and credentials operations."""

    def __init__(self, db_session: AsyncSession):
        super().__init__(User, db_session)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieves a user account matching email address.
        
        Args:
            email: Query email.
            
        Returns:
            Optional[User]: The found user or None.
        """
        result = await self.db.execute(
            select(User).where(User.email == email).where(User.deleted_at.is_(None))
        )
        return result.scalars().first()
