"""Logging middleware."""

# pylint: disable=too-few-public-methods

import logging
from collections.abc import Awaitable, Callable
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)
# log to a file
logging.basicConfig(filename="app.log", level=logging.INFO)


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
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        process_time = response.headers.get("X-Process-Time", "N/A")
        logger.info(
            "%s - %s %s %s %s",
            request_id,
            request.method,
            request.url,
            response.status_code,
            process_time,
        )
        return response
