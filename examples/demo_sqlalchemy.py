
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy import func, case
from sqlalchemy import select, func, cast, Date, desc


DATABASE_URL = "postgresql://user@localhost/dvdrental"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customer"
    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"<Customer(first_name={self.first_name}, last_name={self.last_name})>"

class Inventory(Base):
    """Schema for inventory table."""

    __tablename__ = "inventory"
    inventory_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("film.film_id"))
    store_id: Mapped[int] = mapped_column(Integer, default=1)


class Rental(Base):
    """Schema for rental table."""

    __tablename__ = "rental"
    rental_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("customer.customer_id"),
    )
    inventory_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("inventory.inventory_id"),
    )
    rental_date: Mapped[str] = mapped_column(DateTime)
    return_date: Mapped[str] = mapped_column(DateTime, nullable=True)


class Film(Base):
    """Schema for film table."""

    __tablename__ = "film"
    film_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    rental_duration: Mapped[int] = mapped_column(Integer)

# query table
def get_customers():
    db = SessionLocal()
    return db.query(Customer).all()


def select_customer_by_id(customer_id):
    db = SessionLocal()
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()


def get_inventory_ids_for(
        film_id: int, store_id: int
) -> list[Inventory]:
    db = SessionLocal()
    return db.query(Inventory).filter(Inventory.film_id == film_id, Inventory.store_id == store_id).all()


def get_available_inventory_for_rental(film_id, store_id):
    db = SessionLocal()
    inventory_ids = [
        inventory.inventory_id
        for inventory in (db.query(Inventory).filter(Inventory.film_id == film_id, Inventory.store_id == store_id).all())
    ]
    for inventory_id in inventory_ids:
        result = db.query(Rental).filter(Rental.inventory_id == inventory_id).order_by(Rental.rental_id.desc()).first()
        if not result or result.return_date is not None:
            return inventory_id
    return None


def get_inventory_available_for_rental_v2(
        film_id: int,
        store_id: int
) -> Inventory | None:
    """
    Get one available inventory item for a film at a specific store.

    Args:
        film_id: ID of the film
        store_id: ID of the store

    Returns:
        Available Inventory object, or None if all copies are rented.
    """
    # Subquery: Get all currently rented inventory IDs
    db = SessionLocal()
    rented_inventory_subquery = (
        db.query(Rental.inventory_id)
        .filter(Rental.return_date == None)  # Active rentals only
        .subquery()
    )

    # Find the first available inventory item
    available_inventory = (
        db.query(Inventory)
        .filter(
            Inventory.film_id == film_id,
            Inventory.store_id == store_id,
            ~Inventory.inventory_id.in_(rented_inventory_subquery)
        )
        .first()
    )

    return available_inventory


def get_inventory_available_for_rental_v3(
        film_id: int,
        store_id: int
) -> Inventory | None:
    """
    Get one available inventory item for rental.

    Args:
        film_id: ID of the film to rent
        store_id: ID of the store

    Returns:
        Available Inventory object, or None if all copies are rented.
    """
    db = SessionLocal()
    # Get all currently rented inventory IDs
    rented_inventory_ids = (
        db.query(Rental.inventory_id)
        .filter(Rental.return_date == None)
        .scalar_subquery()
    )

    # Find first available inventory
    return (
        db.query(Inventory)
        .filter(
            Inventory.film_id == film_id,
            Inventory.store_id == store_id,
            ~Inventory.inventory_id.in_(rented_inventory_ids)
        )
        .first()
    )


def get_inventory_available_for_rental_v4(
        film_id: int,
        store_id: int
) -> Inventory | None:
    """Get one available inventory item (most efficient)."""
    db = SessionLocal()
    active_rental = (
        exists()
        .where(Rental.inventory_id == Inventory.inventory_id)
        .where(Rental.return_date == None)
    )

    return (
        db.query(Inventory)
        .filter(
            Inventory.film_id == film_id,
            Inventory.store_id == store_id,
            ~active_rental
        )
        .first()
    )


def get_overdue_rentals_v1():
    """Return all overdue rentals (not returned and past due date)."""
    db = SessionLocal()
    current_date = func.current_date()

    # due_date = rental_date::date + rental_duration
    due_date_expr = func.cast(Rental.rental_date, Date) + Film.rental_duration

    # days_overdue = GREATEST(current_date - due_date, 0)
    days_overdue_expr = func.greatest(
        current_date - due_date_expr,
        0
    )

    query = (
        db.query(
            Rental.rental_id,
            Rental.customer_id,
            Rental.rental_date,
            Inventory.film_id,
            Rental.inventory_id,
            Film.rental_duration,
            due_date_expr.label("due_date"),
            days_overdue_expr.label("days_overdue"),
        )
        .join(Inventory, Inventory.inventory_id == Rental.inventory_id)
        .join(Film, Film.film_id == Inventory.film_id)
        .filter(
            Rental.return_date.is_(None),
            current_date > due_date_expr,
        )
        .order_by(Rental.rental_id.desc())
    )

    return query.all()




def get_overdue_rentals_v2():
    """Return all overdue rentals (not returned and past due date)."""
    with SessionLocal() as db:
        current_date = func.current_date()

        # due_date = rental_date::date + rental_duration
        due_date_expr = cast(Rental.rental_date, Date) + Film.rental_duration

        # days_overdue = GREATEST(current_date - due_date, 0)
        days_overdue_expr = func.greatest(current_date - due_date_expr, 0)

        stmt = (
            select(
                Rental.rental_id,
                Rental.customer_id,
                Rental.rental_date,
                Inventory.film_id,
                Rental.inventory_id,
                Film.rental_duration,
                due_date_expr.label("due_date"),
                days_overdue_expr.label("days_overdue"),
            )
            .join(Inventory, Inventory.inventory_id == Rental.inventory_id)
            .join(Film, Film.film_id == Inventory.film_id)
            .where(
                Rental.return_date.is_(None),
                current_date > due_date_expr,
            )
            .order_by(desc(Rental.rental_id))
        )

        return db.execute(stmt).all()


def main():
    overdue_rentals = get_overdue_rentals_v1()
    print(f"Found {len(overdue_rentals)} overdue rentals")
    print(overdue_rentals[0])

    overdue_rentals = get_overdue_rentals_v2()
    print(f"Found {len(overdue_rentals)} overdue rentals")
    print(overdue_rentals[0].rental_id)

if __name__ == "__main__":
    main()
