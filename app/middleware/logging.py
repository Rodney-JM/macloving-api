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

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["X-Request-ID"] = request_id
        except Exception as e:
            status_code = 500
            
            logger.error(
                "http_error",
                method=request.method,
                path=request.url.path,
                error=str(e)
            )
            raise

        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status=status_code,
            duration_ms=duration_ms,
            user_agent=request.headers.get("user-agent", "")
        )

        return response