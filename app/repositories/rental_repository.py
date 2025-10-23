# app/repositories/rental_repository.py
"""Repository for rental table."""

# pylint: disable=too-few-public-methods
from __future__ import annotations

from typing import TYPE_CHECKING

from app.core.exceptions import (
    NotFoundException,
)
from app.db.schemas import Film, Inventory, Rental
from app.models.rental import RentalOutput
from app.repositories.base_repository import BaseRepository
from app.utils.query_builders import apply_filters

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.orm import Query

    from app.models.rental_filters import RentalFilters


class RentalRepository(BaseRepository):
    """Repository for rental table."""

    def get_rentals_filtered_by(
        self,
        rental_filters: RentalFilters,
    ) -> list[Rental]:
        """Get rentals filtered by custom filters."""
        query: Query = self.db.query(Rental)
        query = apply_filters(
            query=query,
            model=Rental,
            filters=rental_filters,
        )
        return query.all()

    def get_rental(self, rental_id: int) -> Rental | None:
        """Get a rental from its primary ky (rental_id).

        Parameters
        ----------
        rental_id : int
            The ID of the rental to retrieve.

        Returns
        -------
        Rental | None
            The rental corresponding with the given ID
            if it exists, None otherwise.

        """
        return self.db.query(Rental).filter(Rental.rental_id == rental_id).first()

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

    def create_rental_raw(
        self,
        customer_id: int,
        inventory_id: int,
        staff_id: int,
        rental_date: datetime,
    ) -> Rental:
        """Create a new row in rental table."""
        rental = Rental(
            customer_id=customer_id,
            inventory_id=inventory_id,
            staff_id=staff_id,
            rental_date=rental_date,
        )
        self.db.add(rental)
        return rental
