"""Unit tests for RentalService."""

from datetime import UTC, datetime

import pytest

from app.core.exceptions import (
    FilmNotAvailableException,
    NotFoundException,
    RentalAlreadyReturnedException,
)
from app.services.rental_service import RentalService


def test_get_rental_item_success(db_session, multiple_rentals):
    """Test get_rental_item method."""
    service = RentalService(db_session)
    rental = service.get_rental_item(rental_id=multiple_rentals[0].rental_id)

    assert rental is not None
    assert rental.rental_id == 1
    assert rental.customer_id == 1
    assert rental.inventory_id == 1
    assert rental.rental_date == datetime(2025, 1, 15, 10, 30, 0)  # noqa: DTZ001
    assert rental.return_date == datetime(2025, 1, 22, 10, 30, 0)  # noqa: DTZ001


def test_get_rental_item_raises_exception(db_session, multiple_rentals):
    """Test get_rental_item method raises NotFoundException."""
    service = RentalService(db_session)

    with pytest.raises(NotFoundException) as exc_info:
        service.get_rental_item(rental_id=999)

    assert "Rental with id 999 not found" in str(exc_info.value.detail)


def test_return_rental_commits_and_refreshes(db_session, multiple_rentals):
    """Test full transactional return_rental flow."""
    service = RentalService(db_session)

    rental_id = multiple_rentals[2].rental_id
    returned = service.return_rental(rental_id=rental_id)

    assert returned.return_date is not None
    assert isinstance(returned.return_date, datetime)

    # Ensure DB is actually updated (committed)
    reloaded = db_session.query(type(multiple_rentals[2])).get(rental_id)
    assert reloaded.return_date is not None


def test_return_rental_already_returned_raises(db_session, multiple_rentals):
    """Should raise if rental already has a return_date."""
    service = RentalService(db_session)

    with pytest.raises(RentalAlreadyReturnedException) as exc_info:
        service.return_rental(rental_id=multiple_rentals[0].rental_id)

    assert "Rental with id 1 already returned" in str(exc_info.value.detail)


def test_create_rental_success(db_session, multiple_customers_with_rentals):
    """Test create_rental method."""
    service = RentalService(db_session)
    rental = service.create_rental(
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
    service = RentalService(db_session)
    with pytest.raises(FilmNotAvailableException) as exc_info:
        service.create_rental(
            customer_id=multiple_customers_with_rentals[0][1].customer_id,
            film_id=3,
        )
    assert "Film 3 is not available for rental at store 1" in str(exc_info.value.detail)
