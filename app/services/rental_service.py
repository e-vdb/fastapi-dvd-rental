"""Rental service."""


from sqlalchemy.orm import Session

from app.core.exceptions import (
    FilmNotAvailableException,
    NotFoundException,
    RentalAlreadyReturnedException,
)
from app.models.rental import RentalItem
from app.models.rental_filters import RentalFilters
from app.repositories.customer_repository import CustomerRepository
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.rental_repository import RentalRepository
from app.utils.date_utilities import get_today_with_custom_format


class RentalService:
    """A class to manage the rental service."""

    def __init__(self, db: Session) -> None:
        """Initialise the rental service."""
        self._db = db
        self.customer_repo = CustomerRepository(
            db=self._db,
        )
        self.inventory_repo = InventoryRepository(
            db=self._db,
        )
        self.rental_repo = RentalRepository(
            db=self._db,
        )

    def get_rental_item(self, rental_id: int) -> RentalItem:
        """Return rental item."""
        rental = self.rental_repo.get_rental(rental_id)
        if rental is None:
            raise NotFoundException(
                resource="Rental",
                identifier=rental_id,
            )
        return RentalItem.model_validate(rental)

    def get_rentals_filtered_by(self, filters: RentalFilters) -> list[RentalItem]:
        """Get rentals filtered by custom filters."""
        results = self.rental_repo.get_rentals_filtered_by(filters)

        return [RentalItem.model_validate(result) for result in results]

    def return_rental(self, rental_id: int) -> RentalItem:
        """Return a rental and persist the change."""
        rental = self.rental_repo.get_rental(rental_id=rental_id)
        if rental is None:
            raise NotFoundException(
                resource="Rental",
                identifier=rental_id,
            )
        if rental.return_date is not None:
            raise RentalAlreadyReturnedException(
                identifier=rental_id,
            )
        rental.return_date = get_today_with_custom_format()

        # Persist the change
        self._db.commit()
        self._db.refresh(rental)

        return RentalItem.model_validate(rental)

    def create_rental(self, customer_id: int, film_id: int) -> RentalItem:
        """Create and persist a rental transaction."""
        customer = self.customer_repo.get_customer(customer_id)
        inventory = self.inventory_repo.get_inventory_available_for_rental(
            film_id=film_id,
            store_id=customer.store_id,
        )
        if not inventory:
            raise FilmNotAvailableException(
                film_id=film_id,
                store_id=customer.store_id,
            )

        new_rental = self.rental_repo.create_rental_raw(
            customer_id=customer_id,
            inventory_id=inventory.inventory_id,
            staff_id=customer.store_id,
            rental_date=get_today_with_custom_format(),
        )

        # Commit and refresh to persist
        self._db.commit()
        self._db.refresh(new_rental)

        return RentalItem.model_validate(new_rental)
