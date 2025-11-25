"""Filtering model for films."""

from datetime import UTC, datetime
from enum import Enum

from pydantic import ConfigDict, Field

from app.models.base_filters import OrderDirectionEnum, PaginationFilter
from app.models.film import CategoryEnum, RatingEnum


class SortableFilmColum(str, Enum):
    """Sortable columns for films."""

    FILM_ID = "film_id"
    TITLE = "title"
    RELEASE_YEAR = "release_year"


class FilmFilters(PaginationFilter):
    """A filter model for rentals."""

    model_config = ConfigDict(
        use_enum_values=True,
    )

    category: CategoryEnum | None = Field(
        None,
        description="Filter on specific category",
    )

    release_year: int | None = Field(
        None,
        description="Filter on specific release_year",
        ge=1900,
        le=datetime.now(UTC).year,
    )

    rating: RatingEnum | None = Field(
        None,
        description="Filter on specific rating",
    )

    # Sorting configuration
    order_by: SortableFilmColum = Field(
        default=SortableFilmColum.FILM_ID,
        description="Column to sort by",
    )
    order_direction: OrderDirectionEnum = Field(
        default=OrderDirectionEnum.ASC,
        description="Sort order direction",
    )
