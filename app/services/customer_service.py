# app/services/customer_service.py
"""Customer service."""
# pylint: disable=too-few-public-methods
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.customer import CustomerOutput
from app.models.rental import RentalOutput
from app.repositories.customer_repository import CustomerRepository
from app.repositories.rental_repository import RentalRepository


class CustomerService:
    """Customer service for the api."""

    def __init__(self, db: Session) -> None:
        """Initialise the class."""
        self._db = db
        self.customer_repo = CustomerRepository(db=self._db)
        self.rental_repo = RentalRepository(db=self._db)

    def get_customer(self, customer_id: int) -> CustomerOutput:
        """Get a customer from its unique id."""
        customer = self.customer_repo.get_customer(customer_id=customer_id)
        if customer is None:
            raise NotFoundException(
                resource="Customer",
                identifier=customer_id,
            )

        return CustomerOutput.model_validate(customer)

    def get_customer_rentals(self, customer_id: int) -> list[RentalOutput]:
        """Get rentals of a customer."""
        customer = self.customer_repo.get_customer(customer_id=customer_id)
        if customer is None:
            raise NotFoundException(
                resource="Customer",
                identifier=customer_id,
            )
        results = self.rental_repo.get_customer_rentals(customer_id=customer_id)
        return [RentalOutput.model_validate(result) for result in results]
