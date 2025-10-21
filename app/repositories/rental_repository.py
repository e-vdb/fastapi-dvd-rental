# app/repositories/rental_repository.py
"""Repository for rental table."""

# pylint: disable=too-few-public-methods
from __future__ import annotations

from datetime import UTC, datetime

from app.core.exceptions import NotFoundException, ReturnDateAlreadyExistsException
from app.db.schemas import Film, Inventory, Rental
from app.models.rental import RentalItem, RentalOutput
from app.repositories.base_repository import BaseRepository


class RentalRepository(BaseRepository):
    """Repository for rental table."""

    def _get_rental_helper(self, rental_id: int) -> Rental:
        """Get a rental by ID (helper function).

        Parameters
        ----------
        rental_id : int
            The ID of the rental to retrieve.

        Returns
        -------
        Rental
            The rental with the given ID.

        Raises
        ------
        NotFoundException
            If the rental with the given ID does not exist.

        """
        result = self.db.query(Rental).filter(Rental.rental_id == rental_id).first()
        if result is None:
            raise NotFoundException(
                resource="Rental",
                identifier=rental_id,
            )
        return result

    def get_rental_item(self, rental_id: int) -> RentalItem:
        """Get a rental item by ID.

        Parameters
        ----------
        rental_id : int
            The ID of the rental to retrieve.

        Returns
        -------
        RentalItem
            The rental item with the given ID.

        """
        result = self._get_rental_helper(rental_id=rental_id)
        return RentalItem(
            rental_id=result.rental_id,
            customer_id=result.customer_id,
            inventory_id=result.inventory_id,
            rental_date=result.rental_date,
            return_date=result.return_date,
        )

    def return_rental(self, rental_id: int) -> RentalItem:
        """Mark a rental as returned.

        Parameters
        ----------
        rental_id : int
            The ID of the rental to return.

        Returns
        -------
        RentalItem
            The rental item with the return date set.

        Raises
        ------
        NotFoundException
            If the rental with the given ID does not exist.
        ReturnDateAlreadyExistsException
            If the rental has already been returned.

        """
        rental = self._get_rental_helper(rental_id=rental_id)

        if rental.return_date is not None:
            raise ReturnDateAlreadyExistsException(
                identifier=rental_id,
            )
        rental.return_date = datetime.now(tz=UTC)
        self.db.commit()
        self.db.refresh(rental)
        return RentalItem(
            rental_id=rental.rental_id,
            customer_id=rental.customer_id,
            inventory_id=rental.inventory_id,
            rental_date=rental.rental_date,
            return_date=rental.return_date,
        )

    def get_customer_rentals(self, customer_id: int) -> list[RentalOutput]:
        """Get rentals of customer."""
        results = (
            self.db.query(Rental.rental_date, Film.title)
            .join(Inventory, Rental.inventory_id == Inventory.inventory_id)
            .join(Film, Inventory.film_id == Film.film_id)
            .filter(Rental.customer_id == customer_id)
            .all()
        )
        if len(results) == 0:
            raise NotFoundException(
                resource="Customer",
                identifier=customer_id,
            )
        return [
            RentalOutput(
                rental_date=result.rental_date,
                title=result.title,
            )
            for result in results
        ]
