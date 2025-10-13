# app/repositories/rental_repository.py
"""Repository for rental table."""

# pylint: disable=too-few-public-methods
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.db.schemas import Film, Inventory, Rental
from app.models.rental import RentalOutput


class RentalRepository:
    """Repository for rental table."""

    def __init__(self, db: Session) -> None:
        """Initialize the repository."""
        self.db = db

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
