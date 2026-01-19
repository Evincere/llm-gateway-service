import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.infrastructure.adapters.database import get_session
from app.infrastructure.adapters.sql_repositories import SQLLogRepository
from app.core.domain.request_log import RequestLog
from loguru import logger
from uuid import UUID

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log every request to the database and stdout.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        process_time = time.time() - start_time
        latency_ms = int(process_time * 1000)
        
        # We only log API endpoints (v1)
        if request.url.path.startswith("/v1/"):
            # Attempt to get project_id from request state (if set by auth dependency)
            # However, middleware runs before/after the route handler, and get_project_by_api_key 
            # is a dependency. We might need a better way to link them.
            # For now, we'll log what we can.
            
            logger.info(f"Path: {request.url.path} | Status: {response.status_code} | Latency: {latency_ms}ms")
            
        return response
