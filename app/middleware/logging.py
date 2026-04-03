import time
import uuid
from fastapi import Request, Response 
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()
        
        #vinculando o requestid ao contexto de log dessa requisição
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)
        
        try:
            response = await call_next(request)
        except Exception as e:
            duration_ms = round((time.perf_counter() - start) * 1000,2)    
        
        
        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=duration_ms,
            user_agent=request.headers.get("user-agent", "")
        )
        
        response.headers["X-Request-ID"] = request_id
        
        return response