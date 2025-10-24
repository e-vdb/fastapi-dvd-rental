"""Models for the films."""

from enum import Enum

from pydantic import BaseModel, ConfigDict


class RatingEnum(str, Enum):
    """Enum for film ratings."""

    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class CategoryEnum(str, Enum):
    """Enum for film categories."""

    FAMILY = "Family"
    GAMES = "Games"
    ANIMATION = "Animation"
    DOCUMENTARY = "Documentary"
    CLASSICS = "Classics"
    SPORTS = "Sports"
    NEW = "New"
    CHILDREN = "Children"
    MUSIC = "Music"
    TRAVEL = "Travel"
    FOREIGN = "Foreign"
    HORROR = "Horror"
    DRAMA = "Drama"
    ACTION = "Action"
    SCIFI = "Sci - Fi"
    COMEDY = "Comedy"


class FilmModel(BaseModel):
    """Film model."""

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )

    film_id: int
    title: str
    rental_duration: int
    rating: str
    description: str
    release_year: int


class EnrichedFilmModel(FilmModel):
    """Enriched film model."""

    category: CategoryEnum
