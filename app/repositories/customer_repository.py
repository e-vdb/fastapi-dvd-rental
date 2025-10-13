# app/repositories/customer_repository.py
"""Customer repository module."""

# pylint: disable=too-few-public-methods

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.db.schemas import Customer
from app.models.customer import CustomerOutput


class CustomerRepository:
    """Class to interact with customers."""

    def __init__(self, db: Session) -> None:
        """Initialise the customer repository service."""
        self.db = db

    def get_customer(
        self,
        customer_id: int,
        raise_not_found: bool = True,
    ) -> CustomerOutput:
        """Retrieve a customer from the id."""
        customer = (
            self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
        )
        if customer is None and raise_not_found:
            raise NotFoundException(
                resource="Customer",
                identifier=customer_id,
            )

        return CustomerOutput(
            customer_id=customer.customer_id,
            first_name=customer.first_name,
            last_name=customer.last_name,
        )
