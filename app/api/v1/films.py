"""Films API endpoints."""

from fastapi import APIRouter, Depends

from app.api.deps import DatabaseSession
from app.core.logging_config import get_logger
from app.core.security import require_permission
from app.models.film import EnrichedFilmModel, FilmCastResponse, FilmModel
from app.models.filters.film import FilmFilters
from app.models.rental import RentalFilmCountOutput
from app.models.reports import ActorFilmCount, ActorRentalCount
from app.repositories.film_repository import FilmRepository
from app.services.film_service import FilmService

logger = get_logger(__name__)

router = APIRouter(
    prefix="/films",
    tags=["films"],
)


@router.get("/{film_id}/read", response_model=FilmModel | EnrichedFilmModel)
def get_film(
    db: DatabaseSession,
    film_id: int,
    *,
    include_details: bool = False,
) -> FilmModel | EnrichedFilmModel:
    """Retrieve a film by ID."""
    service = FilmService(db)
    return service.get_film(film_id=film_id, include_details=include_details)


@router.get("/", response_model=list[EnrichedFilmModel])
def list_films(
    db: DatabaseSession,
    filters: FilmFilters = Depends(),
) -> list[EnrichedFilmModel]:
    """Retrieve a film by ID."""
    service = FilmService(db)
    return service.list_films(filters=filters)


@router.get("/{film_id}/cast", response_model=FilmCastResponse)
def get_film_cast(
    db: DatabaseSession,
    film_id: int,
) -> FilmCastResponse:
    """Retrieve the cast of a film."""
    service = FilmService(db)
    return service.get_film_cast(film_id=film_id)


@router.get("/{film_id}/availability", response_model=dict)
def get_film_availability(
    db: DatabaseSession,
    film_id: int,
    store_id: int,
) -> dict:
    """Retrieve the availability of a film."""
    service = FilmService(db)
    return {
        "film_id": film_id,
        "available": service.get_available_stock(
            film_id=film_id,
            store_id=store_id,
        ),
    }


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


@router.get("/top-actors", response_model=list[ActorFilmCount])
def get_top_actors(
    db: DatabaseSession,
    top_n: int = 10,
    user: dict = Depends(require_permission("read:reports")),
) -> list[ActorFilmCount]:
    """Retrieve the top actors (most films)."""
    logger.info(
        "User %s requested the %s top actors.",
        user.get("sub"),
        top_n,
    )
    service = FilmRepository(db)
    return service.get_top_actors(limit=top_n)


@router.get("/top-actors-rented", response_model=list[ActorRentalCount])
def get_top_rented_actors(
    db: DatabaseSession,
    top_n: int = 10,
    user: dict = Depends(require_permission("read:reports")),
) -> list[ActorRentalCount]:
    """Retrieve the top actors (most rentals)."""
    logger.info(
        "User %s requested the %s top actors (most rentals).",
        user.get("sub"),
        top_n,
    )
    service = FilmRepository(db)
    return service.get_top_rented_actors(limit=top_n)
