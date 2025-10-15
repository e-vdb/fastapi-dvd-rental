"""Unit tests for CustomerRepository."""

import pytest

from app.core.exceptions import NotFoundException
from app.repositories.customer_repository import CustomerRepository


def test_get_customer_success(db_session, sample_customer):
    """Test successfully retrieving a customer by ID."""
    repository = CustomerRepository(db_session)
    customer = repository.get_customer(sample_customer.customer_id)

    assert customer is not None
    assert customer.customer_id == 1
    assert customer.first_name == "John"
    assert customer.last_name == "Doe"


def test_get_customer_not_found_raises_exception(db_session, sample_customer):
    """Test getting a non-existent customer raises NotFoundException."""
    repository = CustomerRepository(db_session)

    with pytest.raises(NotFoundException) as exc_info:
        repository.get_customer(customer_id=999)

    assert "Customer with id 999 not found" in str(exc_info.value.detail)
