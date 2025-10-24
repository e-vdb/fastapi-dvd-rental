# app/repositories/film_repository.py
"""Film repository."""

# pylint: disable=too-few-public-methods, not-callable, duplicate-code

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Sequence, func, select

from app.db.schemas import (
    Actor,
    CategoryOrm,
    Film,
    FilmActor,
    FilmCategoryOrm,
    Inventory,
    Rental,
)
from app.models.rental import RentalFilmCountOutput
from app.models.reports import ActorFilmCount, ActorRentalCount
from app.repositories.base_repository import BaseRepository
from app.utils.query_builders import apply_filters_map

if TYPE_CHECKING:
    from app.models.filters.film import FilmFilters


class FilmRepository(BaseRepository):
    """Class to manage film data."""

    def get_film(self, film_id: int) -> Film | None:
        """Get a film from its unique id."""
        stmt = select(Film).where(Film.film_id == film_id)
        return self.db.execute(stmt).scalars().first()

    def get_film_with_details(self, film_id: int) -> Sequence:
        """Get a film from its unique id with details.

        The query joins the film, film_category, and category tables
         to get the film details.

        """
        stmt = (
            select(
                Film.film_id,
                Film.title,
                Film.rental_duration,
                Film.rating,
                Film.release_year,
                Film.description,
                CategoryOrm.name.label("category"),
            )
            .join(FilmCategoryOrm, Film.film_id == FilmCategoryOrm.film_id)
            .join(CategoryOrm, CategoryOrm.category_id == FilmCategoryOrm.category_id)
            .where(Film.film_id == film_id)
        )
        return self.db.execute(stmt).first()

    def list_films(self, filters: FilmFilters) -> Sequence:
        """Return a list of films that match the specified filters."""
        stmt = (
            select(
                Film.film_id,
                Film.title,
                CategoryOrm.name.label("category"),
                Film.description,
                Film.rating,
                Film.release_year,
                Film.rental_duration,
            )
            .join(FilmCategoryOrm, FilmCategoryOrm.film_id == Film.film_id)
            .join(CategoryOrm, CategoryOrm.category_id == FilmCategoryOrm.category_id)
        )

        # Build filter map for all relevant fields
        filter_map = {
            "rating": Film.rating,
            "title": Film.title,
            "category": CategoryOrm.name,
            "film_id": Film.film_id,
            "release_year": Film.release_year,
        }

        stmt = apply_filters_map(
            stmt=stmt,
            filters=filters,
            filter_map=filter_map,
        )

        return self.db.execute(stmt).all()

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
