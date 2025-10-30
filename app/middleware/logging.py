"""Logging middleware."""

# pylint: disable=too-few-public-methods
from collections.abc import Awaitable, Callable
from uuid import uuid4

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging_config import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests with unique request IDs.

    This middleware generates a unique ID for each request, logs request details
    including method, URL, status code, and processing time, and adds the request
    ID to response headers.

    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Process the request and log its details."""
        request_id = str(uuid4())
        # Bind context for all loggers during this request
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=str(request.url.path),
        )

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        process_time = response.headers.get("X-Process-Time", "N/A")

        logger.info(
            "request_handled",
            status_code=response.status_code if "response" in locals() else "N/A",
            process_time=process_time,
        )

        # Clean up contextvars after request (important!)
        structlog.contextvars.clear_contextvars()
        return response
