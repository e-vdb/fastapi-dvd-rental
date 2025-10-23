"""Rentals API endpoints."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, Query

from app.api.deps import DatabaseSession  # noqa: TCH001
from app.core.security import require_permission
from app.models.rental import OverdueRental, RentalCreate, RentalItem
from app.models.rental_filters import (  # noqa: TCH001
    OverdueRentalFilters,
    RentalFilters,
)
from app.services.rental_service import RentalService

router = APIRouter(
    prefix="/rentals",
    tags=["rentals"],
)
logger = logging.getLogger(__name__)
logging.basicConfig(filename="app.log", level=logging.INFO)


@router.get("/{rental_id}/read", response_model=RentalItem)
def get_rental_item(
    db: DatabaseSession,
    rental_id: int,
    user: dict = Depends(require_permission("read:rentals")),
) -> RentalItem:
    """Retrieve a rental by ID."""
    logger.info(
        "User %s accessed rental %s",
        user.get("sub"),
        rental_id,
    )
    service = RentalService(db)
    return service.get_rental_item(rental_id=rental_id)


@router.get("/", response_model=list[RentalItem])
def get_rentals_filtered_by(
    db: DatabaseSession,
    rental_filters: RentalFilters = Query(
        ...,
    ),
    _user: dict = Depends(require_permission("read:rentals")),
) -> list[RentalItem]:
    """Get rentals filtered by custom filters."""
    logger.info(
        "User %s accessed rentals with custom filter %s",
        _user.get("sub"),
        rental_filters.model_dump_json(),
    )
    service = RentalService(db=db)
    return service.get_rentals_filtered_by(
        filters=rental_filters,
    )


@router.get("/overdue", response_model=list[OverdueRental])
def get_overdue_rentals(
    db: DatabaseSession,
    filters: OverdueRentalFilters = Depends(),
    _user: dict = Depends(require_permission("read:rentals")),
) -> list[OverdueRental]:
    """Get overdue rentals filtered by custom filters."""
    logger.info(
        "User %s fetched overdue rentals with custom filter %s",
        _user.get("sub"),
        filters.model_dump_json(),
    )
    service = RentalService(db)
    return service.get_overdue_rentals(filters)


@router.patch("/{rental_id}/return", response_model=RentalItem)
def return_rental(
    db: DatabaseSession,
    rental_id: int,
    user: dict = Depends(require_permission("write:rentals")),
) -> RentalItem:
    """Return a rental."""
    logger.info(
        "User %s returned rental %s",
        user.get("sub"),
        rental_id,
    )
    service = RentalService(db)
    return service.return_rental(rental_id=rental_id)


@router.post("/", response_model=RentalItem, status_code=201)
def create_rental(
    db: DatabaseSession,
    rental_data: RentalCreate,
    _user: dict = Depends(require_permission("write:rentals")),
) -> RentalItem:
    """Create a new rental.

    Requires write:rentals permission..
    """
    logger.info(
        "User %s creating a rental for customer %s and film %s",
        _user.get("sub"),
        rental_data.customer_id,
        rental_data.film_id,
    )
    service = RentalService(db)
    return service.create_rental(
        customer_id=rental_data.customer_id,
        film_id=rental_data.film_id,
    )
