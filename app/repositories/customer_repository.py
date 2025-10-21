# app/repositories/customer_repository.py
"""Customer repository module."""

# pylint: disable=too-few-public-methods

from app.core.exceptions import NotFoundException
from app.db.schemas import Customer
from app.models.customer import CustomerOutput
from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    """Class to interact with customers."""

    def get_customer(
        self,
        customer_id: int,
    ) -> CustomerOutput:
        """Retrieve a customer from the id."""
        customer = (
            self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
        )
        if customer is None:
            raise NotFoundException(
                resource="Customer",
                identifier=customer_id,
            )

        return CustomerOutput(
            customer_id=customer.customer_id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            store_id=customer.store_id,
        )
