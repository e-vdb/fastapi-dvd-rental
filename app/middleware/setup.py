"""Configuration and setup for application middleware."""

from fastapi import FastAPI

from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.timing import ProcessTimeMiddleware


def setup_middleware(app: FastAPI) -> None:
    """Configure all middleware for the application."""
    app.add_middleware(ProcessTimeMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
