"""Models for the endpoints input and responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RentalOutput(BaseModel):
    """Model for the rental output."""

    model_config = ConfigDict(from_attributes=True)

    rental_id: int
    inventory_id: int
    rental_date: datetime
    return_date: datetime | None = None
    title: str


class RentalFilmCountOutput(BaseModel):
    """Model for the rental film count output."""

    title: str
    count: int


class RentalItem(BaseModel):
    """Model for the rental item."""

    model_config = ConfigDict(from_attributes=True)

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


class OverdueRental(BaseModel):
    """Model for the overdue rental."""

    rental_id: int
    customer_id: int
    inventory_id: int
    film_id: int
    rental_duration: int
    rental_date: datetime = Field(
        ...,
        title="Rental date",
        description="Date of the rental.",
    )
    due_date: datetime = Field(
        ...,
        title="Rental date",
        description="Date of the rental.",
    )
    days_overdue: int
