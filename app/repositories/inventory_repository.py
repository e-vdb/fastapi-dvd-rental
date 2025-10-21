# app/repositories/inventory_repository.py
"""Repository for inventory table."""

# pylint: disable=too-few-public-methods,singleton-comparison
from __future__ import annotations

from app.db.schemas import Inventory, Rental
from app.repositories.base_repository import BaseRepository


class InventoryRepository(BaseRepository):
    """Repository for inventory table."""

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
