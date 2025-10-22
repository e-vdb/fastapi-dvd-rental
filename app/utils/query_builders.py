"""Utility functions for queries."""


from sqlalchemy.orm import Query

from app.models.base_filters import BaseFilter


def apply_filters(query: Query, model: type, filters: BaseFilter) -> Query:
    """Apply filters, ordering, and pagination dynamically."""
    # --- Dynamic filtering based on fields ---
    for field_name, value in filters.model_dump().items():
        if value is None:
            continue
        if field_name in ("skip", "limit", "order_by", "order_direction"):
            continue

        column_name = getattr(model, field_name, None)
        if column_name is not None:
            query = query.filter(column_name == value)

    # --- Ordering ---
    order_col = getattr(model, filters.order_by, None)
    if order_col is not None:
        if filters.order_direction == "asc":
            query = query.order_by(order_col.asc())
        else:
            query = query.order_by(order_col.desc())

    # --- Pagination ---
    return query.offset(filters.skip).limit(filters.limit)
