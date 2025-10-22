"""Filtering model for rentals."""


from .base_filters import BaseFilter


class RentalFilters(BaseFilter):
    """A filter model for rentals."""

    order_by: str = "rental_id"
    customer_id: int | None = None
