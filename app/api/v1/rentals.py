"""Rentals API endpoints."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from app.api.deps import DatabaseSession  # noqa: TCH001
from app.core.security import require_permission
from app.models.rental import RentalOutput
from app.repositories.rental_repository import RentalRepository

router = APIRouter(
    prefix="/rentals",
    tags=["rentals"],
)
logger = logging.getLogger(__name__)
logging.basicConfig(filename="app.log", level=logging.INFO)


@router.get("/{customer_id}", response_model=list[RentalOutput])
def get_customer_rentals(
    db: DatabaseSession,
    customer_id: int,
    user: dict = Depends(require_permission("read:rentals")),
) -> list[RentalOutput]:
    """Retrieve rentals for a given customer."""
    logger.info(
        "User %s accessed customer %s",
        user.get("sub"),
        customer_id,
    )
    service = RentalRepository(db)
    return service.get_customer_rentals(customer_id=customer_id)
