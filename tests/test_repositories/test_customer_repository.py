"""Unit tests for CustomerRepository."""


from app.repositories.customer_repository import CustomerRepository


def test_get_customer_success(db_session, sample_customer):
    """Test successfully retrieving a customer by ID."""
    repository = CustomerRepository(db_session)
    customer = repository.get_customer(sample_customer.customer_id)

    assert customer is not None
    assert customer.customer_id == 1
    assert customer.first_name == "John"
    assert customer.last_name == "Doe"


def test_get_customer_not_found(db_session, sample_customer):
    """Test getting a non-existent customer returns None."""
    repository = CustomerRepository(db_session)
    customer = repository.get_customer(999)
    assert customer is None
