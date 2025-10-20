"""Models for the endpoints input and responses."""

from datetime import datetime

from pydantic import BaseModel


class RentalOutput(BaseModel):
    """Model for the rental output."""

    rental_date: datetime
    title: str


class RentalFilmCountOutput(BaseModel):
    """Model for the rental film count output."""

    title: str
    count: int
