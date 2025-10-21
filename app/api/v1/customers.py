"""Customers API endpoints."""

import logging

from fastapi import APIRouter, Depends

from app.api.deps import DatabaseSession
from app.core.security import require_permission
from app.models.customer import CustomerOutput
from app.models.rental import RentalOutput
from app.repositories.customer_repository import CustomerRepository
from app.repositories.rental_repository import RentalRepository

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)

logger = logging.getLogger(__name__)
logging.basicConfig(filename="app.log", level=logging.INFO)


@router.get("/{customer_id}", response_model=CustomerOutput)
def get_customer(
    customer_id: int,
    db: DatabaseSession,
    user: dict = Depends(require_permission("read:customers")),
) -> CustomerOutput:
    """Retrieve a customer by ID."""
    # Log who accessed the customer data
    logger.info(
        "User %s accessed customer %s",
        user.get("sub"),
        customer_id,
    )
    service = CustomerRepository(db)
    return service.get_customer(customer_id=customer_id)


@router.get("/{customer_id}/rentals", response_model=list[RentalOutput])
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
