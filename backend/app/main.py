from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.core.config import settings
from app.infrastructure.logging.logger import logger
from app.core.middleware import CorrelationIdMiddleware, RateLimitingMiddleware
import app.infrastructure.database.base

# Endpoint Routers
from app.api.v1.endpoints.health import router as health_router, health_check
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.dashboard import router as dashboard_router
from app.api.v1.endpoints.agents import router as agents_router
from app.api.v1.endpoints.learning import router as learning_router
from app.api.v1.endpoints.workflows import router as workflows_router
from app.api.v1.endpoints.websocket import router as websocket_router
from app.api.v1.endpoints.demo import router as demo_router

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Global custom exception handler for structured JSON error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    correlation_id = getattr(request.state, "correlation_id", "none")
    request_id = getattr(request.state, "request_id", "none")
    
    logger.error("Unhandled global exception occurred", error=str(exc), correlation_id=correlation_id)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred on the server.",
            "details": str(exc),
            "timestamp": time.time(),
            "correlation_id": correlation_id,
            "request_id": request_id
        }
    )

# Middlewares (Executed in reverse order of addition)
app.add_middleware(RateLimitingMiddleware)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register direct health check
app.add_api_route("/health", health_check, methods=["GET"], tags=["Status"])

# Register v1 router endpoints
app.include_router(health_router, prefix="/api/v1", tags=["Status"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(agents_router, prefix="/api/v1", tags=["Agents"])
app.include_router(learning_router, prefix="/api/v1", tags=["Learning"])
app.include_router(workflows_router, prefix="/api/v1/workflows", tags=["Workflows"])
app.include_router(websocket_router, prefix="", tags=["WebSockets"])
app.include_router(demo_router, prefix="/api/v1/demo", tags=["Demo"])

# Startup lifecycle log
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing Life-GPS Operating System Backend", 
                app_name=settings.APP_NAME, 
                environment=settings.APP_ENV, 
                debug_mode=settings.DEBUG)
