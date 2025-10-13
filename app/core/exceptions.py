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
