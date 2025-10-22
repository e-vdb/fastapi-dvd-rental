"""Filtering model for rentals."""

from enum import Enum

from pydantic import ConfigDict, Field

from .base_filters import OrderDirectionEnum, PaginationFilter


class SortableRentalColumn(str, Enum):
    """Sortable columns for rentals."""

    RENTAL_ID = "rental_id"
    CUSTOMER_ID = "customer_id"
    INVENTORY_ID = "inventory_id"
    RENTAL_DATE = "rental_date"
    RETURN_DATE = "return_date"


class RentalFilters(PaginationFilter):
    """A filter model for rentals."""

    model_config = ConfigDict(
        use_enum_values=True,
    )

    # Filtering options
    customer_id: int | None = Field(None, description="Filter by customer ID")
    inventory_id: int | None = Field(None, description="Filter by inventory ID")

    # Sorting configuration
    order_by: SortableRentalColumn = Field(
        default=SortableRentalColumn.RENTAL_ID,
        description="Column to sort by",
    )
    order_direction: OrderDirectionEnum = Field(
        default=OrderDirectionEnum.ASC,
        description="Sort order direction",
    )
