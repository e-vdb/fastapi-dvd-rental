"""Films API endpoints."""

import logging

from fastapi import APIRouter, Depends

from app.api.deps import DatabaseSession
from app.core.security import require_permission
from app.models.rental import RentalFilmCountOutput
from app.repositories.film_repository import FilmRepository

router = APIRouter(
    prefix="/films",
    tags=["films"],
)
logger = logging.getLogger(__name__)
logging.basicConfig(filename="app.log", level=logging.INFO)


@router.get("/top", response_model=list[RentalFilmCountOutput])
def get_top_rented_films(
    db: DatabaseSession,
    top_n: int = 10,
    user: dict = Depends(require_permission("read:reports")),
) -> list[RentalFilmCountOutput]:
    """Retrieve the top rented films."""
    logger.info(
        "User %s requested the %s top rented films.",
        user.get("sub"),
        top_n,
    )
    service = FilmRepository(db)
    return service.get_most_rented(limit=top_n)
