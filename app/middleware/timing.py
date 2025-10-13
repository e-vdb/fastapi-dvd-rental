"""Middleware for tracking request processing time."""

# pylint: disable=too-few-public-methods

import time
from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Middleware to measure and add request processing time to response headers.

    This middleware calculates the time taken to process each request and adds
    it to the response headers as 'X-Process-Time' in seconds.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Process the request and add timing information to the response."""
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
