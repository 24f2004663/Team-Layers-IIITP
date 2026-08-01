from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.connection import AsyncSessionLocal
from app.infrastructure.logging.logger import logger

@asynccontextmanager
async def transaction_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations with auto rollback/commit.
    
    Yields:
        AsyncSession: Active transaction-wrapped database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error("Transaction failed, rolling back active changes", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()
