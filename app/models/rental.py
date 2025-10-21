"""Models for the endpoints input and responses."""

from datetime import datetime

from pydantic import BaseModel, Field


class RentalOutput(BaseModel):
    """Model for the rental output."""

    rental_date: datetime
    title: str


class RentalFilmCountOutput(BaseModel):
    """Model for the rental film count output."""

    title: str
    count: int


class RentalItem(BaseModel):
    """Model for the rental item."""

    rental_id: int
    customer_id: int
    inventory_id: int
    rental_date: datetime = Field(
        ...,
        title="Rental date",
        description="Date of the rental.",
    )
    return_date: datetime | None = Field(
        None,
        title="Return date",
        description="Date of the return if any.",
    )


class RentalCreate(BaseModel):
    """Request model for creating a rental."""

    customer_id: int = Field(..., gt=0, description="ID of the customer")
    film_id: int = Field(..., gt=0, description="ID of the film to rent")
