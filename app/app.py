"""Fast API application."""

# pylint: disable=unused-argument

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.deps import CurrentUser
from app.api.v1 import customers, films, rentals
from app.core.config import get_settings
from app.core.exception_handlers import (
    not_found_exception_handler,
    validation_exception_handler,
)
from app.core.exceptions import CustomValidationError, NotFoundException
from app.core.logging_config import get_logger, setup_logging
from app.middleware.setup import setup_middleware


@asynccontextmanager
async def lifespan() -> AsyncGenerator:
    """Initialise the application start up.

    Handles startup and shutdown events.
    """
    settings = get_settings()
    logger = get_logger(__name__)
    setup_logging(json_logs=not settings.debug)

    logger.info(
        "Application starting up",
        extra={
            "app_name": settings.app_name,
            "debug": settings.debug,
            "log_level": settings.log_level,
        },
    )

    yield

    logger.info("Application shutting down")


def create_app() -> FastAPI:
    """Create the restapi."""
    settings = get_settings()
    logger = get_logger(__name__)
    setup_logging(json_logs=not settings.debug)

    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )
    setup_middleware(app)
    # Register exception handlers
    app.add_exception_handler(
        exc_class_or_status_code=NotFoundException,
        handler=not_found_exception_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=CustomValidationError,
        handler=validation_exception_handler,
    )

    app.include_router(
        customers.router,
        prefix="/api/v1",
    )

    app.include_router(
        router=rentals.router,
        prefix="/api/v1",
    )

    app.include_router(
        router=films.router,
        prefix="/api/v1",
    )

    @app.get("/")
    def read_root() -> dict[str, str]:
        """Read root endpoint."""
        return {"Hello": "World"}

    @app.get("/api/public")
    def public() -> dict[str, str]:
        """Get public endpoint.

        No access token required to access this route.
        """
        return {
            "status": "success",
            "msg": (
                "Hello from a public endpoint! You don't need to be "
                "authenticated to see this."
            ),
        }

    # new code 👇
    @app.get("/api/private")
    def private(user: CurrentUser) -> dict:
        """Get private endpoint that requires authentication.

        Args:
            user: Current authenticated user from JWT token.

        Returns:
            Token payload containing user information.

        Raises:
            HTTPException: 401 if no token provided, 403 if token invalid.

        """
        return {
            "status": "success",
            "message": "Hello from a private endpoint! You are authenticated.",
            "user": user,
        }

    logger.info("FastAPI application created successfully")
    return app


fastapi_app = create_app()
