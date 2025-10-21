"""Rentals API endpoints."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from app.api.deps import DatabaseSession  # noqa: TCH001
from app.core.security import require_permission
from app.models.rental import RentalItem
from app.repositories.rental_repository import RentalRepository

router = APIRouter(
    prefix="/rentals",
    tags=["rentals"],
)
logger = logging.getLogger(__name__)
logging.basicConfig(filename="app.log", level=logging.INFO)


@router.get("/{rental_id}", response_model=RentalItem)
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
    service = RentalRepository(db)
    return service.get_rental_item(rental_id=rental_id)


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
    service = RentalRepository(db)
    return service.return_rental(rental_id=rental_id)
