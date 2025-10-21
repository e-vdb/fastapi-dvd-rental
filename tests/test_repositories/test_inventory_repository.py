"""Unit tests for InventoryRepository."""


from app.repositories.inventory_repository import InventoryRepository


def test_get_inventory_available_for_rental(
    db_session,
    multiple_customers_with_rentals,
):
    """Test get_inventory_available_for_rental method."""
    repository = InventoryRepository(db_session)
    inventory = repository.get_inventory_available_for_rental(
        film_id=1,
        store_id=1,
    )
    assert inventory is not None
    assert inventory.inventory_id == 1

    # test with not available film
    inventory = repository.get_inventory_available_for_rental(
        film_id=3,
        store_id=1,
    )
    assert inventory is None
