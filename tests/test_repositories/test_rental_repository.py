"""Unit tests for RentalRepository."""

# pylint: disable=no-member

from datetime import UTC, datetime

import pytest

from app.core.exceptions import (
    FilmNotAvailableException,
    NotFoundException,
    ReturnDateAlreadyExistsException,
)
from app.models.rental_filters import RentalFilters
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


def test_get_rental_item_success(db_session, multiple_rentals):
    """Test get_rental_item method."""
    repository = RentalRepository(db_session)
    rental = repository.get_rental_item(rental_id=multiple_rentals[0].rental_id)

    assert rental is not None
    assert rental.rental_id == 1
    assert rental.customer_id == 1
    assert rental.inventory_id == 1
    assert rental.rental_date == datetime(2025, 1, 15, 10, 30, 0)  # noqa: DTZ001
    assert rental.return_date == datetime(2025, 1, 22, 10, 30, 0)  # noqa: DTZ001


def test_get_rental_item_raises_exception(db_session, multiple_rentals):
    """Test get_rental_item method raises NotFoundException."""
    repository = RentalRepository(db_session)

    with pytest.raises(NotFoundException) as exc_info:
        repository.get_rental_item(rental_id=999)

    assert "Rental with id 999 not found" in str(exc_info.value.detail)


def test_return_rental_raises_exception(db_session, multiple_rentals):
    """Test return_rental method raises ReturnDateAlreadyExistsException."""
    repository = RentalRepository(db_session)
    with pytest.raises(ReturnDateAlreadyExistsException) as exc_info:
        repository.return_rental(rental_id=multiple_rentals[0].rental_id)

    assert "Rental with id 1 already returned" in str(exc_info.value.detail)


def test_return_rental_success(db_session, multiple_rentals):
    """Test return_rental method."""
    repository = RentalRepository(db_session)
    rental = repository.return_rental(rental_id=multiple_rentals[2].rental_id)

    assert rental is not None
    assert rental.rental_id == 3
    assert rental.customer_id == 3
    assert rental.inventory_id == 3
    assert rental.rental_date == datetime(2025, 1, 15, 10, 30, 0)  # noqa: DTZ001


def test_create_rental_success(db_session, multiple_customers_with_rentals):
    """Test create_rental method."""
    repository = RentalRepository(db_session)
    rental = repository.create_rental(
        customer_id=multiple_customers_with_rentals[0][1].customer_id,
        film_id=1,
    )
    today = datetime.now(tz=UTC)

    assert rental is not None
    assert rental.rental_id == 7
    assert rental.customer_id == 2
    assert rental.inventory_id == 1
    assert rental.rental_date.year == today.year
    assert rental.rental_date.month == today.month
    assert rental.rental_date.day == today.day
    assert rental.rental_date.hour == today.hour
    assert rental.rental_date.minute == today.minute
    assert rental.return_date is None


def test_create_rental_raises_exception(db_session, multiple_customers_with_rentals):
    """Test create_rental method raises FilmNotAvailableException."""
    repository = RentalRepository(db_session)
    with pytest.raises(FilmNotAvailableException) as exc_info:
        repository.create_rental(
            customer_id=multiple_customers_with_rentals[0][1].customer_id,
            film_id=3,
        )
    assert "Film 3 is not available for rental at store 1" in str(exc_info.value.detail)


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
