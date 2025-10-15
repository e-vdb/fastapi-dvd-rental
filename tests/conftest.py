"""Pytest configuration and shared fixtures."""

from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.app import app
from app.db.schemas import Base, Customer, Film, Inventory, Rental
from app.db.session import get_db

# Use in-memory SQLite for fast unit tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine (session-scoped).

    Creates all tables once per test session for performance.
    """
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_engine):
    """Create a fresh database session for each test.

    Each test gets a clean database state with automatic rollback.
    This ensures test isolation.

    Args:
        test_engine: SQLAlchemy engine fixture.

    Yields:
        SQLAlchemy Session instance.

    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
    )
    session = session_factory()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create a test client with database override.

    This fixture overrides the get_db dependency to use the test database
    instead of the production database.

    Args:
        db_session: Test database session fixture.

    Yields:
        FastAPI TestClient instance.

    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ==================== Data Fixtures ====================


@pytest.fixture
def sample_customer(db_session):
    """Create a sample customer for testing.

    Args:
        db_session: Test database session.

    Returns:
        Customer instance with id=1.

    """
    customer = Customer(
        customer_id=1,
        first_name="John",
        last_name="Doe",
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer


@pytest.fixture
def sample_film(db_session):
    """Create a sample film for testing.

    Args:
        db_session: Test database session.

    Returns:
        Film instance with id=1.

    """
    film = Film(
        film_id=1,
        title="The Shawshank Redemption",
    )
    db_session.add(film)
    db_session.commit()
    db_session.refresh(film)
    return film


@pytest.fixture
def sample_inventory(db_session, sample_film):
    """Create a sample inventory item for testing.

    Args:
        db_session: Test database session.
        sample_film: Film fixture.

    Returns:
        Inventory instance with id=1.

    """
    inventory = Inventory(
        inventory_id=1,
        film_id=sample_film.film_id,
    )
    db_session.add(inventory)
    db_session.commit()
    db_session.refresh(inventory)
    return inventory


@pytest.fixture
def sample_rental(db_session, sample_customer, sample_inventory):
    """Create a sample rental for testing.

    Args:
        db_session: Test database session.
        sample_customer: Customer fixture.
        sample_inventory: Inventory fixture.

    Returns:
        Rental instance with id=1.

    """
    rental = Rental(
        rental_id=1,
        customer_id=sample_customer.customer_id,
        inventory_id=sample_inventory.inventory_id,
        rental_date=datetime(2025, 1, 15, 10, 30, 0, tzinfo=UTC),
    )
    db_session.add(rental)
    db_session.commit()
    db_session.refresh(rental)
    return rental


@pytest.fixture
def multiple_customers(db_session):
    """Create multiple customers for testing list operations.

    Args:
        db_session: Test database session.

    Returns:
        List of Customer instances.

    """
    customers = [
        Customer(customer_id=1, first_name="John", last_name="Doe"),
        Customer(customer_id=2, first_name="Jane", last_name="Smith"),
        Customer(customer_id=3, first_name="Bob", last_name="Johnson"),
    ]
    db_session.add_all(customers)
    db_session.commit()
    for customer in customers:
        db_session.refresh(customer)
    return customers


@pytest.fixture
def customer_with_rentals(db_session, sample_customer):
    """Create a customer with multiple rentals for testing.

    Args:
        db_session: Test database session.
        sample_customer: Customer fixture.

    Returns:
        Tuple of (customer, list of rentals).

    """
    # Create films
    films = [
        Film(film_id=1, title="The Shawshank Redemption"),
        Film(film_id=2, title="The Godfather"),
        Film(film_id=3, title="The Dark Knight"),
    ]
    db_session.add_all(films)

    # Create inventory
    inventories = [
        Inventory(inventory_id=1, film_id=1),
        Inventory(inventory_id=2, film_id=2),
        Inventory(inventory_id=3, film_id=3),
    ]
    db_session.add_all(inventories)

    # Create rentals
    base_date = datetime(2025, 1, 1, tzinfo=UTC)
    rentals = [
        Rental(
            rental_id=1,
            customer_id=sample_customer.customer_id,
            inventory_id=1,
            rental_date=base_date,
        ),
        Rental(
            rental_id=2,
            customer_id=sample_customer.customer_id,
            inventory_id=2,
            rental_date=base_date + timedelta(days=7),
        ),
        Rental(
            rental_id=3,
            customer_id=sample_customer.customer_id,
            inventory_id=3,
            rental_date=base_date + timedelta(days=14),
        ),
    ]
    db_session.add_all(rentals)
    db_session.commit()

    for rental in rentals:
        db_session.refresh(rental)

    return sample_customer, rentals


@pytest.fixture
def multiple_customers_with_rentals(db_session, multiple_customers):
    """
    Create multiple customers with multiple rentals for testing.

    Args:
        db_session: Test database session.
        multiple_customers: Customer fixture.

    Returns:
        Tuple of (list of customers, list of rentals).

    """
    # Create films
    films = [
        Film(film_id=1, title="The Shawshank Redemption"),
        Film(film_id=2, title="The Godfather"),
        Film(film_id=3, title="The Dark Knight"),
    ]
    db_session.add_all(films)

    # Create inventory
    inventories = [
        Inventory(inventory_id=1, film_id=1),
        Inventory(inventory_id=2, film_id=2),
        Inventory(inventory_id=3, film_id=3),
    ]
    db_session.add_all(inventories)

    # Create rentals
    base_date = datetime(2025, 1, 1, tzinfo=UTC)
    rentals = [
        Rental(
            rental_id=1,
            customer_id=multiple_customers[0].customer_id,
            inventory_id=1,
            rental_date=base_date,
        ),
        Rental(
            rental_id=2,
            customer_id=multiple_customers[1].customer_id,
            inventory_id=2,
            rental_date=base_date,
        ),
        Rental(
            rental_id=3,
            customer_id=multiple_customers[2].customer_id,
            inventory_id=3,
            rental_date=base_date,
        ),
        Rental(
            rental_id=4,
            customer_id=multiple_customers[0].customer_id,
            inventory_id=2,
            rental_date=base_date + timedelta(days=7),
        ),
        Rental(
            rental_id=5,
            customer_id=multiple_customers[1].customer_id,
            inventory_id=3,
            rental_date=base_date + timedelta(days=7),
        ),
        Rental(
            rental_id=6,
            customer_id=multiple_customers[2].customer_id,
            inventory_id=3,
            rental_date=base_date + timedelta(days=14),
        ),
    ]
    db_session.add_all(rentals)
    db_session.commit()

    for rental in rentals:
        db_session.refresh(rental)

    return multiple_customers, rentals
