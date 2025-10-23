"""Utility functions for queries."""


from typing import Any

from sqlalchemy.orm import Query
from sqlalchemy.sql import Select

from app.models.base_filters import OrderDirectionEnum, PaginationFilter


def apply_filters(query: Query, model: type, filters: PaginationFilter) -> Query:
    """Apply filters, ordering, and pagination dynamically.

    Parameters
    ----------
    query: Query
        Base SQLAlchemy query
    model: type
        SQLAlchemy model class (e.g., Rental)
    filters: PaginationFilter
        Pydantic filter model with filter parameters

    Returns
    -------
    Query
        SQLAlchemy query with filters, ordering, and pagination applied

    """
    # Fields to exclude from automatic filtering
    excluded_fields = {"skip", "limit", "order_by", "order_direction"}

    # --- Dynamic filtering based on fields ---
    for field_name, value in filters.model_dump().items():
        if value is None:
            continue
        if field_name in excluded_fields:
            continue

        column_name = getattr(model, field_name, None)
        if column_name is not None:
            query = query.filter(column_name == value)

    # --- Ordering ---
    order_col = getattr(model, filters.order_by, None)
    if order_col is not None:
        if filters.order_direction == OrderDirectionEnum.ASC.value:
            query = query.order_by(order_col.asc())
        else:
            query = query.order_by(order_col.desc())

    # --- Pagination ---
    return query.offset(filters.skip).limit(filters.limit)


def apply_filters_map(
    stmt: Select,
    filters: PaginationFilter,
    filter_map: dict[str, Any],
    excluded_fields: set[str] | None = None,
) -> Select:
    """Apply dynamic filters, ordering, and pagination using a column map."""
    excluded_fields = excluded_fields or {
        "skip",
        "limit",
        "order_by",
        "order_direction",
    }

    # --- Filtering ---
    for field_name, value in filters.model_dump().items():
        if value is None or field_name in excluded_fields:
            continue
        column_expr = filter_map.get(field_name)
        if column_expr is not None:
            stmt = stmt.where(column_expr == value)

    # --- Ordering ---
    order_by = getattr(filters, "order_by", None)
    if order_by:
        order_col = filter_map.get(order_by)
        if order_col is not None:
            direction = getattr(filters, "order_direction", "ASC").upper()
            stmt = stmt.order_by(
                order_col.asc() if direction == "ASC" else order_col.desc(),
            )

    # --- Pagination and return ---
    return stmt.offset(getattr(filters, "skip", 0)).limit(
        getattr(filters, "limit", 100),
    )
