# app/services/film_service.py
"""Film service."""
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.film import (
    ActorResponse,
    EnrichedFilmModel,
    FilmCastResponse,
    FilmModel,
)
from app.models.filters.film import FilmFilters
from app.repositories.actor_repository import ActorRepository
from app.repositories.film_repository import FilmRepository
from app.repositories.inventory_repository import InventoryRepository


class FilmService:
    """The service related to films."""

    def __init__(self, db: Session) -> None:
        """Initialise the class."""
        self._db = db
        self.film_repo = FilmRepository(db=self._db)
        self.actor_repo = ActorRepository(db=self._db)
        self.inventory_repo = InventoryRepository(db=self._db)

    def get_film(
        self,
        film_id: int,
        *,
        include_details: bool = False,
    ) -> FilmModel | EnrichedFilmModel:
        """Retrieve a film by ID.

        Returns
        -------
        FilmModel | EnrichedFilmModel
            The film.

        Raises
        ------
        NotFoundException
            If the film is not found.

        """
        if not include_details:
            film = self.film_repo.get_film(
                film_id=film_id,
            )
            if film is None:
                raise NotFoundException(
                    resource="Film",
                    identifier=film_id,
                )
            return FilmModel.model_validate(film)
        film = self.film_repo.get_film_with_details(
            film_id=film_id,
        )
        if film is None:
            raise NotFoundException(
                resource="Film",
                identifier=film_id,
            )
        return EnrichedFilmModel.model_validate(film)

    def list_films(self, filters: FilmFilters) -> list[EnrichedFilmModel]:
        """Retrieve a list of films.

        Returns
        -------
        list[EnrichedFilmModel]
            The list of films filtered on the provided filters.

        """
        results = self.film_repo.list_films(
            filters=filters,
        )
        return [EnrichedFilmModel.model_validate(result) for result in results]

    def get_film_cast(self, film_id: int) -> FilmCastResponse:
        """Get the cast of a given film."""
        film = self.film_repo.get_film(
            film_id=film_id,
        )
        if film is None:
            raise NotFoundException(
                resource="Film",
                identifier=film_id,
            )
        actors = [
            ActorResponse.model_validate(
                actor,
            )
            for actor in self.actor_repo.get_cast(film_id=film_id)
        ]
        return FilmCastResponse(
            film_id=film_id,
            actors=actors,
        )

    def get_available_stock(self, film_id: int, store_id: int) -> int:
        """Get the available stock of a film."""
        film = self.film_repo.get_film(
            film_id=film_id,
        )
        if film is None:
            raise NotFoundException(
                resource="Film",
                identifier=film_id,
            )
        return self.inventory_repo.get_available_inventory_count(
            film_id=film_id,
            store_id=store_id,
        )
