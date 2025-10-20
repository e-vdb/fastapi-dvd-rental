"""Test suite for the films router of the api."""


def test_get_endpoints_unauthorized(client):
    """Test accessing protected endpoints without auth returns 401."""
    endpoints = ["top", "top-actors", "top-actors-rented"]
    for endpoint in endpoints:
        response = client.get(f"/films/{endpoint}")
        assert response.status_code == 401
        assert response.json()["detail"] == "Requires authentication"


def test_get_endpoints_authorized_without_permissions(client_with_customer_auth):
    """Test accessing endpoints without permissions returns 403."""
    endpoints = ["top", "top-actors", "top-actors-rented"]
    for endpoint in endpoints:
        response = client_with_customer_auth.get(f"/films/{endpoint}")
        assert response.status_code == 403
        assert response.json()["detail"] == "Permission 'read:reports' required"


def test_get_top_success(client_with_analyst_auth, multiple_customers_with_rentals):
    """Test accessing top endpoint with permissions returns 200."""
    response = client_with_analyst_auth.get("films/top")
    assert response.status_code == 200
    top_rented = response.json()
    assert len(top_rented) == 3


def test_get_top_actors_success(client_with_analyst_auth, sample_multiple_films_actors):
    """Test accessing top-actors endpoint with permissions returns 200."""
    response = client_with_analyst_auth.get("films/top-actors", params={"top_n": 5})
    assert response.status_code == 200
    top_actors = response.json()
    assert len(top_actors) == 5
    assert top_actors[0]["first_name"] == "Bruce"
    assert top_actors[0]["last_name"] == "Willis"
    assert top_actors[0]["film_count"] == 3


def test_get_top_rented_actors_success(
    client_with_analyst_auth,
    multiple_customers_with_rentals_and_actors,
):
    """Test top-actors-rented endpoint with permissions returns 200."""
    response = client_with_analyst_auth.get(
        "films/top-actors-rented",
        params={"top_n": 5},
    )
    assert response.status_code == 200
    top_actors = response.json()
    assert len(top_actors) == 5
    assert top_actors[0]["first_name"] == "Bruce"
    assert top_actors[0]["last_name"] == "Willis"
    assert top_actors[0]["rental_count"] == 6
