# app/repositories/actor_repository.py
"""Actor repository."""

# pylint: disable=too-few-public-methods, not-callable

from __future__ import annotations

from sqlalchemy import Sequence, select

from app.db.schemas import Actor, Film, FilmActor
from app.repositories.base_repository import BaseRepository


class ActorRepository(BaseRepository):
    """Class to perform actor-related queries."""

    def get_cast(self, film_id: int) -> Sequence:
        """Retrieve the cast of a film."""
        stmt = (
            select(
                Actor.first_name,
                Actor.last_name,
            )
            .join(FilmActor, FilmActor.actor_id == Actor.actor_id)
            .join(Film, Film.film_id == FilmActor.film_id)
            .where(Film.film_id == film_id)
        )

        return self.db.execute(stmt).all()
