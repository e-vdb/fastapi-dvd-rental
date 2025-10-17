"""Reports models."""

from pydantic import BaseModel


class ActorFilmCount(BaseModel):
    """Actor film count model."""

    actor_id: int
    first_name: str
    last_name: str
    film_count: int


class ActorRentalCount(BaseModel):
    """Actor rental count model."""

    actor_id: int
    first_name: str
    last_name: str
    rental_count: int
