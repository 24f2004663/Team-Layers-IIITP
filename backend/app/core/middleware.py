import time
from uuid import uuid4
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from collections import defaultdict
from app.infrastructure.logging.logger import logger

# Simple in-memory rate limiter store
# Keys: (ip, current_minute_timestamp)
# Value: count (int)
RATE_LIMIT_STORE = defaultdict(int)
LIMIT_PER_MINUTE = 100

class RateLimitingMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware protecting demo setups."""
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        current_minute = int(time.time() / 60)
        
        limit_key = (client_ip, current_minute)
        RATE_LIMIT_STORE[limit_key] += 1
        
        if RATE_LIMIT_STORE[limit_key] > LIMIT_PER_MINUTE:
            logger.warning("Rate limit exceeded for IP", client_ip=client_ip, limit=LIMIT_PER_MINUTE)
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests. Please slow down.",
                    "details": f"Limit of {LIMIT_PER_MINUTE} requests per minute exceeded.",
                    "timestamp": time.time()
                }
            )
            
        return await call_next(request)

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Middleware attaching request-level Correlation and Request IDs to headers and context."""
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        
        # Resolve IDs
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid4())
        workflow_id = request.headers.get("X-Workflow-ID") or "none"
        
        # Attach to request state for access in endpoints
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id
        
        # Execute request pipeline
        try:
            response = await call_next(request)
        except Exception as e:
            latency = time.time() - start_time
            logger.error(
                "Request pipeline crashed",
                path=request.url.path,
                request_id=request_id,
                correlation_id=correlation_id,
                workflow_id=workflow_id,
                latency=latency,
                error=str(e)
            )
            raise e
            
        latency = time.time() - start_time
        
        # Add to response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id
        
        logger.info(
            "Request completed",
            path=request.url.path,
            method=request.method,
            status_code=response.status_code,
            request_id=request_id,
            correlation_id=correlation_id,
            workflow_id=workflow_id,
            latency=latency
        )
        
        return response
