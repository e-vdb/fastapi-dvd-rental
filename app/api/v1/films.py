"""Films API endpoints."""

from fastapi import APIRouter

from app.api.deps import DatabaseSession
from app.models.rental import RentalFilmCountOutput
from app.repositories.film_repository import FilmRepository

router = APIRouter(
    prefix="/films",
    tags=["films"],
)


@router.get("/films/top", response_model=list[RentalFilmCountOutput])
def get_top_rented_films(
    db: DatabaseSession,
    top_n: int = 10,
) -> list[RentalFilmCountOutput]:
    """Retrieve the top rented films."""
    service = FilmRepository(db)
    return service.get_most_rented(limit=top_n)
