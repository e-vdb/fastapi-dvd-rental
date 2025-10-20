"""Unit tests for FilmRepository."""

from app.repositories.film_repository import FilmRepository


def test_get_most_rented_success(db_session, multiple_customers_with_rentals):
    """Test successfully retrieving the most rented films."""
    repository = FilmRepository(db_session)
    top_rented = repository.get_most_rented(limit=5)

    assert top_rented is not None
    assert len(top_rented) == 3
    assert top_rented[0].title == "The Dark Knight"
    assert top_rented[0].count == 3
    assert top_rented[1].title == "The Godfather"
    assert top_rented[1].count == 2
    assert top_rented[2].title == "The Shawshank Redemption"
    assert top_rented[2].count == 1


def test_get_top_actors_success(db_session, sample_multiple_films_actors):
    """Test successfully retrieving the top actors (most films)."""
    repository = FilmRepository(db_session)
    top_actors_most_films = repository.get_top_actors(limit=5)
    assert top_actors_most_films is not None
    assert len(top_actors_most_films) == 5
    assert top_actors_most_films[0].first_name == "Bruce"
    assert top_actors_most_films[0].last_name == "Willis"
    assert top_actors_most_films[0].film_count == 3


def test_get_top_rented_actors_success(
    db_session,
    multiple_customers_with_rentals_and_actors,
):
    """Test successfully retrieving the top actors (most rentals)."""
    repository = FilmRepository(db_session)
    top_rented_actors = repository.get_top_rented_actors(limit=5)
    assert top_rented_actors is not None
    assert len(top_rented_actors) == 5
    assert top_rented_actors[0].first_name == "Bruce"
    assert top_rented_actors[0].last_name == "Willis"
    assert top_rented_actors[0].rental_count == 6
