"""Test suite for the customer service."""

import pytest

from app.core.exceptions import NotFoundException
from app.services.customer_service import CustomerService


def test_get_customer_not_found_raises_exception(db_session, sample_customer):
    """Test getting a non-existent customer raises NotFoundException."""
    service = CustomerService(db_session)

    with pytest.raises(NotFoundException) as exc_info:
        service.get_customer(customer_id=999)

    assert "Customer with id 999 not found" in str(exc_info.value.detail)
