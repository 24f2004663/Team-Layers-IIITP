from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.connection import get_db_session_with_retry
from app.infrastructure.database.health import ping_database
from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db_session_with_retry)):
    """Health check endpoint evaluating readiness of external dependencies."""
    
    database_ok = await ping_database(db)
    gemini_configured = settings.GOOGLE_API_KEY not in ("", "your_gemini_api_key_here", "mock_key")
    
    status_code = "ok" if (database_ok and gemini_configured) else "degraded"
    
    return {
        "status": status_code,
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "components": {
            "database": "connected" if database_ok else "disconnected",
            "gemini_api": "configured" if gemini_configured else "not_configured"
        }
    }

