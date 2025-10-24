"""Unit tests for ActorRepository."""


from app.repositories.actor_repository import ActorRepository


def test_get_cast_success(db_session, sample_multiple_films_actors):
    """Test getting the cast of a film."""
    repository = ActorRepository(db_session)
    cast = repository.get_cast(film_id=1)
    expected_cast = [
        {"first_name": "Bruce", "last_name": "Willis"},
        {"first_name": "Keanu", "last_name": "Reeves"},
        {"first_name": "Tom", "last_name": "Hanks"},
    ]
    assert cast is not None
    assert len(cast) == 3
    for actor, expected_actor in zip(cast, expected_cast, strict=False):
        assert actor.first_name is not None
        assert actor.first_name == expected_actor["first_name"]
        assert actor.last_name is not None
        assert actor.last_name == expected_actor["last_name"]


def test_get_cast_returns_empty_list(db_session, sample_multiple_films_actors):
    """Test getting the cast of a film not in the database returns an empty list."""
    repository = ActorRepository(db_session)
    cast = repository.get_cast(film_id=4)
    assert cast is not None
    assert len(cast) == 0
