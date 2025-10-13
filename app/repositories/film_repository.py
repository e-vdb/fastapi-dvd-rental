# app/repositories/film_repository.py
"""Film repository."""

# pylint: disable=too-few-public-methods
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import func

from app.db.schemas import Film, Inventory, Rental
from app.models.rental import RentalFilmCountOutput

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class FilmRepository:
    """Class to manage film data."""

    def __init__(self, db: Session) -> None:
        """Initialise the repository."""
        self.db = db

    def get_most_rented(self, limit: int) -> list[RentalFilmCountOutput]:
        """Retrieve the top rented films."""
        results = (
            self.db.query(Film.title, func.count(Rental.rental_id))
            .join(Inventory, Rental.inventory_id == Inventory.inventory_id)
            .join(Film, Inventory.film_id == Film.film_id)
            .group_by(Film.film_id)
            .order_by(func.count(Film.film_id).desc())
            .limit(limit)
            .all()
        )
        return [
            RentalFilmCountOutput(
                title=result[0],
                count=result[1],
            )
            for result in results
        ]
