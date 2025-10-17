"""Schemas for the database tables."""

# pylint: disable=too-few-public-methods

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all schemas."""


class Customer(Base):
    """Schema for customer table."""

    __tablename__ = "customer"
    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"<Customer(first_name={self.first_name}, last_name={self.last_name})>"


class Actor(Base):
    """Schema for actor table."""

    __tablename__ = "actor"
    actor_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"<Actor(first_name={self.first_name}, last_name={self.last_name})>"


class FilmActor(Base):
    """Schema for actor table."""

    __tablename__ = "film_actor"
    actor_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    film_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


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


class Inventory(Base):
    """Schema for inventory table."""

    __tablename__ = "inventory"
    inventory_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("film.film_id"))


class Film(Base):
    """Schema for film table."""

    __tablename__ = "film"
    film_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
