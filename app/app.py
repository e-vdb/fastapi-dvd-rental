"""Fast API application."""

from fastapi import FastAPI, Security

from app.api.v1 import customers, films, rentals
from app.core.auth import VerifyToken
from app.core.exception_handlers import (
    not_found_exception_handler,
    validation_exception_handler,
)
from app.core.exceptions import CustomValidationError, NotFoundException
from app.middleware.setup import setup_middleware

app = FastAPI(title="DVD Rental API")
auth = VerifyToken()
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
def private(auth_result: dict = Security(auth.verify)) -> dict:
    """Get private endpoint.

    A valid access token is required to access this route.
    """
    return auth_result
