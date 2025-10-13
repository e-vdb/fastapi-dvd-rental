"""Global exception handlers for the application."""


from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import NotFoundException


async def not_found_exception_handler(
    request: Request,  # noqa: ARG001, pylint: disable=unused-argument
    exc: NotFoundException,
) -> JSONResponse:
    """Handle NotFoundException globally.

    Args:
        request: The incoming request.
        exc: The NotFoundException instance.

    Returns:
        JSON response with 404 status code.

    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )
