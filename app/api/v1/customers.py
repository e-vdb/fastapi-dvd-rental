"""Customers API endpoints."""

import logging
from http.client import HTTPException

from fastapi import APIRouter, Depends, status

from app.api.deps import DatabaseSession
from app.core.security import require_customer, require_permission
from app.models.customer import CustomerOutput
from app.models.rental import RentalOutput
from app.repositories.rental_repository import RentalRepository
from app.services.customer_service import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)

logger = logging.getLogger(__name__)
logging.basicConfig(filename="app.log", level=logging.INFO)


@router.get("/me", response_model=CustomerOutput)
def get_current_customer(
    db: DatabaseSession,
    user: dict = Depends(require_customer(None)),
) -> CustomerOutput:
    """Retrieve the current customer."""
    logger.info(
        "User %s accessed their own customer data",
        user.get("sub"),
    )
    service = CustomerService(db)
    customer_id_from_token = user.get("https://fastapiexample.com/customer_id")
    if not customer_id_from_token:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return service.get_customer(
        customer_id=customer_id_from_token,
    )


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
    service = CustomerService(db)
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
