"""Fast API application."""

from fastapi import FastAPI

from app.api.v1 import customers, films, rentals
from app.core.exception_handlers import (
    not_found_exception_handler,
    validation_exception_handler,
)
from app.core.exceptions import CustomValidationError, NotFoundException
from app.middleware.setup import setup_middleware

app = FastAPI(title="DVD Rental API")
setup_middleware(app)
# Register exception handlers
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(CustomValidationError, validation_exception_handler)

app.include_router(
    customers.router,
)

app.include_router(
    router=rentals.router,
)

app.include_router(
    router=films.router,
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Read root endpoint."""
    return {"Hello": "World"}
