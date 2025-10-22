"""Utility functions for queries."""


from sqlalchemy.orm import Query

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
