"""Unit tests for RentalRepository."""

# pylint: disable=no-member, duplicate-code

from datetime import UTC, datetime

import pytest

from app.core.exceptions import (
    NotFoundException,
)
from app.db.schemas import Rental
from app.models.rental_filters import OverdueRentalFilters, RentalFilters
from app.repositories.rental_repository import RentalRepository


def test_get_customer_rentals_success(db_session, customer_with_rentals):
    """Test get_customer_rentals method."""
    repository = RentalRepository(db_session)
    rentals = repository.get_customer_rentals(
        customer_id=customer_with_rentals[0].customer_id,
    )

    assert rentals is not None
    assert len(rentals) == 3
    assert rentals[0].rental_date == datetime(2025, 1, 1)  # noqa: DTZ001
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


def test_get_rental_success(db_session, multiple_rentals):
    """Test get_rental_item method."""
    repository = RentalRepository(db_session)
    rental = repository.get_rental(rental_id=multiple_rentals[0].rental_id)

    assert rental is not None
    assert rental.rental_id == 1
    assert rental.customer_id == 1
    assert rental.inventory_id == 1
    assert rental.rental_date == datetime(2025, 1, 15, 10, 30, 0)  # noqa: DTZ001
    assert rental.return_date == datetime(2025, 1, 22, 10, 30, 0)  # noqa: DTZ001


def test_get_rental_item_returns_none(db_session, multiple_rentals):
    """Test get_rental_item method returns None if not rental."""
    repository = RentalRepository(db_session)
    rental = repository.get_rental(rental_id=999)

    assert rental is None


def test_create_rental_raw_adds_object_to_session(
    db_session,
    multiple_customers_with_rentals,
):
    """Test create_rental_raw adds a Rental to the session but does not commit."""
    repo = RentalRepository(db_session)
    rental = repo.create_rental_raw(
        customer_id=1,
        inventory_id=1,
        staff_id=1,
        rental_date=datetime.now(tz=UTC),
    )

    assert isinstance(rental, Rental)
    assert rental.customer_id == 1
    assert rental.inventory_id == 1

    # not committed yet
    db_session.rollback()
    found = db_session.query(Rental).filter_by(customer_id=1, inventory_id=1).first()
    assert found is None


def test_get_rentals_filtered_by_success(db_session, multiple_rentals):
    """Test get_rentals_filtered_by method."""
    repository = RentalRepository(db_session)

    # test sorting ascending
    rentals = repository.get_rentals_filtered_by(
        rental_filters=RentalFilters(
            order_direction="asc",
        ),
    )
    assert rentals is not None
    assert len(rentals) == 3
    assert rentals[0].rental_id == 1
    assert rentals[1].rental_id == 2
    assert rentals[2].rental_id == 3

    # test sorting descending
    rentals = repository.get_rentals_filtered_by(
        rental_filters=RentalFilters(
            order_direction="desc",
        ),
    )
    assert rentals is not None
    assert len(rentals) == 3
    assert rentals[0].rental_id == 3
    assert rentals[1].rental_id == 2
    assert rentals[2].rental_id == 1

    # filter on customer 1 only
    rentals = repository.get_rentals_filtered_by(
        rental_filters=RentalFilters(
            customer_id=1,
        ),
    )
    assert rentals is not None
    assert len(rentals) == 1
    assert rentals[0].customer_id == 1


def test_get_overdue_rentals(db_session, multiple_rentals):
    """Test get_rentals_filtered_by method."""
    repository = RentalRepository(db_session)

    overdue_rentals = repository.get_overdue_rentals(
        filters=OverdueRentalFilters(
            order_direction="desc",
            inventory_id=3,
        ),
    )
    assert overdue_rentals is not None
    assert len(overdue_rentals) == 1
    assert overdue_rentals[0].rental_id == 3
