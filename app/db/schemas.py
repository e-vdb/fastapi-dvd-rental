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
    store_id: Mapped[int] = mapped_column(Integer, default=1)

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
    rental_date: Mapped[DateTime] = mapped_column(DateTime)
    return_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    staff_id: Mapped[int] = mapped_column(Integer, default=1)


class Inventory(Base):
    """Schema for inventory table."""

    __tablename__ = "inventory"
    inventory_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("film.film_id"))
    store_id: Mapped[int] = mapped_column(Integer, default=1)


class Film(Base):
    """Schema for film table."""

    __tablename__ = "film"
    film_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    rental_duration: Mapped[int] = mapped_column(Integer, default=3)
    rating: Mapped[str] = mapped_column(String, default=3)
    description: Mapped[str] = mapped_column(String, nullable=True)
    release_year: Mapped[int] = mapped_column(Integer, default=2025)


class CategoryOrm(Base):
    """Schema for category table."""

    __tablename__ = "category"
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="PG-13")


class FilmCategoryOrm(Base):
    """Schema for film_category table."""

    __tablename__ = "film_category"
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    film_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
