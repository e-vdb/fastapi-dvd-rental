"""Customers API endpoints."""

from fastapi import APIRouter

from app.api.deps import DatabaseSession
from app.models.customer import CustomerOutput
from app.repositories.customer_repository import CustomerRepository

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.get("/{customer_id}", response_model=CustomerOutput)
def get_customer(customer_id: int, db: DatabaseSession) -> CustomerOutput:
    """Retrieve a customer by ID."""
    service = CustomerRepository(db)
    return service.get_customer(customer_id=customer_id)
