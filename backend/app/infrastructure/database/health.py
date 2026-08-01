from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.infrastructure.logging.logger import logger

async def ping_database(db: AsyncSession) -> bool:
    """Performs a quick database connectivity ping.
    
    Args:
        db: Active AsyncSession.
        
    Returns:
        bool: True if connection is alive, False otherwise.
    """
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error("Database connection ping failed", error=str(e))
        return False
