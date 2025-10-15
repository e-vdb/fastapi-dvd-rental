"""Unit tests for RentalRepository."""

from datetime import datetime

import pytest

from app.core.exceptions import NotFoundException
from app.repositories.rental_repository import RentalRepository


def test_get_customer_rentals_success(db_session, customer_with_rentals):
    """Test get_customer_rentals method."""
    repository = RentalRepository(db_session)
    rentals = repository.get_customer_rentals(
        customer_id=customer_with_rentals[0].customer_id,
    )

    assert rentals is not None
    assert len(rentals) == 3
    assert rentals[0].rental_date == datetime(2025, 1, 1)
    assert rentals[0].title == "The Shawshank Redemption"


def test_get_customer_rentals_not_found_raises_exception(
    db_session,
    customer_with_rentals,
):
    """Test get_customer_rentals method raises NotFoundException."""
    repository = RentalRepository(db_session)

    with pytest.raises(NotFoundException) as exc_info:
        repository.get_customer_rentals(customer_id=999)

    assert "Customer with id 999 not found" in str(exc_info.value.detail)
