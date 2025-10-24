# app/repositories/inventory_repository.py
"""Repository for inventory table."""

# pylint: disable=too-few-public-methods,singleton-comparison
from __future__ import annotations

from typing import TYPE_CHECKING

from app.db.schemas import Inventory, Rental
from app.repositories.base_repository import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy.orm import Query


class InventoryRepository(BaseRepository):
    """Repository for inventory table."""

    def _build_available_inventory_query(
        self,
        film_id: int,
        store_id: int,
    ) -> Query:
        """Build a query to get available inventory."""
        rented_inventory_ids = (
            self.db.query(Rental.inventory_id)
            .filter(
                Rental.return_date == None,  # noqa: E711
            )
            .scalar_subquery()
        )

        return self.db.query(Inventory).filter(
            Inventory.film_id == film_id,
            Inventory.store_id == store_id,
            ~Inventory.inventory_id.in_(rented_inventory_ids),
        )

    def get_available_inventory_count(
        self,
        film_id: int,
        store_id: int,
    ) -> int:
        """Get the count of available inventory."""
        return self._build_available_inventory_query(film_id, store_id).count()

    def get_inventory_available_for_rental(
        self,
        film_id: int,
        store_id: int,
    ) -> Inventory | None:
        """Get one available inventory item (optimized query)."""
        rented_inventory_ids = (
            self.db.query(Rental.inventory_id)
            .filter(
                Rental.return_date == None,  # noqa: E711
            )
            .scalar_subquery()
        )

        return (
            self.db.query(Inventory)
            .filter(
                Inventory.film_id == film_id,
                Inventory.store_id == store_id,
                ~Inventory.inventory_id.in_(rented_inventory_ids),
            )
            .first()
        )
