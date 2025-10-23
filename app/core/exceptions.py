"""Custom application exceptions."""
from __future__ import annotations

from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """Exception raised when a resource is not found."""

    def __init__(self, resource: str, identifier: int | str) -> None:
        """Initialize the NotFoundException.

        Parameters
        ----------
        resource: str
            The name of the resource (e.g., "Customer", "Rental").
        identifier:  int | str
            The identifier that was not found.

        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id {identifier} not found",
        )


class CustomValidationError(Exception):
    """A class for custom validation exception."""

    def __init__(self, message: str) -> None:
        """Initialise the class."""
        self.message = message


class UnauthorizedException(HTTPException):
    """A class for unauthorized exception."""

    def __init__(self, detail: str) -> None:
        """Return HTTP 403."""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    """A class for unauthenticated exception."""

    def __init__(self) -> None:
        """Return HTTP 401."""
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires authentication",
        )


class RentalAlreadyReturnedException(HTTPException):
    """Exception raised when a rental is already returned."""

    def __init__(self, identifier: int | str) -> None:
        """Initialize the ReturnDateAlreadyExistsException.

        Parameters
        ----------
        identifier: int | str
            The identifier of the rental that was already returned.

        """
        super().__init__(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Rental with id {identifier} already returned",
        )


class FilmNotAvailableException(HTTPException):
    """Exception raised when a film has no available copies for rental."""

    def __init__(self, film_id: int, store_id: int) -> None:
        """Initialise the FilmNotAvailableException."""
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Film {film_id} is not available for rental at store {store_id}",
        )
