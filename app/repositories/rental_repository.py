# app/repositories/rental_repository.py
"""Repository for rental table."""

# pylint: disable=too-few-public-methods
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Date, Sequence, cast, func, select

from app.core.exceptions import (
    NotFoundException,
)
from app.db.schemas import Film, Inventory, Rental
from app.models.rental import RentalOutput
from app.repositories.base_repository import BaseRepository
from app.utils.query_builders import apply_filters, apply_filters_map

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.orm import Query

    from app.models.rental_filters import OverdueRentalFilters, RentalFilters


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

    def get_overdue_rentals(self, filters: OverdueRentalFilters) -> Sequence:
        """Get overdue rentals filtered.

        To achieve this, we use a SQL query with the following steps:

        1. Select the relevant columns from the rental table
        2. Join the inventory and film tables to get the film details
        3. Filter the rentals to only include those that are overdue
        4. Apply the filters to the query using the apply_filters_map function
        5. Return the results

        Parameters
        ----------
        filters : OverdueRentalFilters
            The filters to apply to the query.

        Returns
        -------
        Sequence
            The overdue rentals filtered.

        """
        current_date = func.current_date()  # pylint: disable=not-callable

        if self.db.bind.dialect.name == "sqlite":
            due_date_expr = func.date(
                Rental.rental_date,
                func.concat(  # pylint: disable=not-callable
                    "+",
                    Film.rental_duration,
                    " day",
                ),
            )
            days_overdue_expr = func.greatest(
                func.julianday(current_date) - func.julianday(due_date_expr),
                0,
            )
        else:
            # due_date = rental_date::date + rental_duration
            due_date_expr = cast(Rental.rental_date, Date) + Film.rental_duration

            # Compute days_overdue as GREATEST(current_date - due_date, 0)
            days_overdue_expr = func.greatest(current_date - due_date_expr, 0)

        stmt = (
            select(
                Rental.rental_id,
                Rental.customer_id,
                Rental.rental_date,
                Inventory.film_id,
                Rental.inventory_id,
                Film.rental_duration,
                due_date_expr.label("due_date"),
                days_overdue_expr.label("days_overdue"),
            )
            .join(Inventory, Inventory.inventory_id == Rental.inventory_id)
            .join(Film, Film.film_id == Inventory.film_id)
            .where(
                Rental.return_date.is_(None),
                current_date > due_date_expr,
            )
        )

        # Build filter map for all relevant fields
        filter_map = {
            "rental_id": Rental.rental_id,
            "customer_id": Rental.customer_id,
            "inventory_id": Rental.inventory_id,
            "film_id": Inventory.film_id,
            "rental_date": Rental.rental_date,
            "due_date": due_date_expr,
            "days_overdue": days_overdue_expr,
        }

        # Apply standard Rental filters
        stmt = apply_filters_map(
            stmt=stmt,
            filters=filters,
            filter_map=filter_map,
        )

        return self.db.execute(stmt).all()
