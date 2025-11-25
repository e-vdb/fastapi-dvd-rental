# app/repositories/customer_repository.py
"""Customer repository module."""

# pylint: disable=too-few-public-methods

from app.db.schemas import Customer
from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    """Class to interact with customers."""

    def get_customer(
        self,
        customer_id: int,
    ) -> Customer:
        """Retrieve a customer from the id."""
        return (
            self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
        )
