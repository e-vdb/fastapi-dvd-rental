"""Base model for filtering."""

from enum import Enum

from pydantic import BaseModel, Field


class OrderDirectionEnum(Enum):
    """Enum for the order direction."""

    ASC = "asc"
    DESC = "desc"


class PaginationFilter(BaseModel):
    """Basic filter model."""

    skip: int = Field(
        default=0,
        ge=0,
        description="Number of records to skip",
    )
    limit: int = Field(
        default=10,
        ge=1,
        description="Maximum records to return",
    )


class OrderFilter(BaseModel):
    """Order filter model."""

    order_direction: OrderDirectionEnum = Field(
        default=OrderDirectionEnum.ASC,
        description="The order direction to order by",
    )
    order_by: str = Field(
        ...,
        description="Column to order by",
    )
