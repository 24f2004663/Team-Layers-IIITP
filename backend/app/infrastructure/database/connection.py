import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import DBAPIError
from app.core.config import settings
from app.infrastructure.logging.logger import logger

# Async engine for PostgreSQL with robust pool configurations
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db_session_with_retry(max_retries: int = 3, backoff: float = 0.5) -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection yield method for database sessions with automatic retry logic.
    
    Args:
        max_retries: Maximum number of reconnection attempts.
        backoff: Base sleep duration for exponential backoff.
        
    Yields:
        AsyncSession: Active database session.
    """
    retries = 0
    while retries < max_retries:
        try:
            async with AsyncSessionLocal() as session:
                try:
                    yield session
                    break  # Success, exit retry loop
                except DBAPIError as e:
                    logger.error("DBAPIError during database session operation; rolling back", error=str(e))
                    await session.rollback()
                    raise
                except Exception as e:
                    logger.error("Unhandled error in database session; rolling back", error=str(e))
                    await session.rollback()
                    raise
        except (DBAPIError, OSError) as conn_err:
            retries += 1
            if retries >= max_retries:
                logger.error("Database connection retries exhausted. Failed to establish session.", error=str(conn_err))
                raise conn_err
            sleep_time = backoff * (2 ** retries)
            logger.warning(f"Database session initiation failed. Retrying in {sleep_time}s...", error=str(conn_err), retry=retries)
            await asyncio.sleep(sleep_time)
