"""Rentals API endpoints."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import DatabaseSession
from app.models.rental import RentalOutput
from app.repositories.rental_repository import RentalRepository

router = APIRouter(
    prefix="/rentals",
    tags=["rentals"],
)


@router.get("/{customer_id}", response_model=list[RentalOutput])
def get_customer_rentals(customer_id: int, db: DatabaseSession) -> list[RentalOutput]:
    """Retrieve rentals for a given customer."""
    service = RentalRepository(db)
    return service.get_customer_rentals(customer_id=customer_id)
