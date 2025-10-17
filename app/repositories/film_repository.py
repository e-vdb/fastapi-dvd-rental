# app/repositories/film_repository.py
"""Film repository."""

# pylint: disable=too-few-public-methods, not-callable

from __future__ import annotations

from sqlalchemy import func

from app.db.schemas import Actor, Film, FilmActor, Inventory, Rental
from app.models.rental import RentalFilmCountOutput
from app.models.reports import ActorFilmCount, ActorRentalCount
from app.repositories.base_repository import BaseRepository


class FilmRepository(BaseRepository):
    """Class to manage film data."""

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

    def get_top_actors(self, limit: int) -> list[ActorFilmCount]:
        """Retrieve the top actors (most films)."""
        results = (
            self.db.query(
                Actor.actor_id,
                Actor.first_name,
                Actor.last_name,
                func.count(FilmActor.film_id),
            )
            .join(FilmActor, Actor.actor_id == FilmActor.actor_id)
            .group_by(Actor.actor_id)
            .order_by(func.count(FilmActor.film_id).desc())
            .limit(limit)
            .all()
        )
        return [
            ActorFilmCount(
                actor_id=result[0],
                first_name=result[1],
                last_name=result[2],
                film_count=result[3],
            )
            for result in results
        ]

    def get_top_rented_actors(self, limit: int) -> list[ActorRentalCount]:
        """Retrieve the top actors (most rentals)."""
        results = (
            self.db.query(
                Actor.actor_id,
                Actor.first_name,
                Actor.last_name,
                func.count(Film.film_id),
            )
            .select_from(Rental)
            .join(Inventory, Rental.inventory_id == Inventory.inventory_id)
            .join(Film, Inventory.film_id == Film.film_id)
            .join(FilmActor, FilmActor.film_id == Film.film_id)
            .join(Actor, Actor.actor_id == FilmActor.actor_id)
            .group_by(Actor.actor_id)
            .order_by(func.count(Film.film_id).desc())
            .limit(limit)
            .all()
        )
        return [
            ActorRentalCount(
                actor_id=result[0],
                first_name=result[1],
                last_name=result[2],
                rental_count=result[3],
            )
            for result in results
        ]
