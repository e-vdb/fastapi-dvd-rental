"""Test suite for the rentals router of the api."""


def test_get_customer_rentals_unauthorized(client):
    """Test accessing protected endpoint without auth returns 401."""
    response = client.get("/api/v1/rentals/1")
    assert response.status_code == 401
    assert response.json()["detail"] == "Requires authentication"


def test_get_customer_rentals_authorized_without_permissions(client_with_customer_auth):
    """Test accessing customer_id endpoint without permissions returns 403."""
    response = client_with_customer_auth.get("/api/v1/rentals/1")
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission 'read:rentals' required"


def test_get_customer_rentals_authorized_with_permissions(
    client_with_staff_auth,
    customer_with_rentals,
):
    """Test accessing customer_id endpoint with permissions returns 200."""
    response = client_with_staff_auth.get("/api/v1/rentals/1")
    assert response.status_code == 200
    rentals = response.json()
    assert rentals is not None
    assert len(rentals) == 3
    assert rentals[0]["title"] == "The Shawshank Redemption"


def test_get_rental_unauthorized(client):
    """Test accessing protected endpoint without auth returns 401."""
    response = client.get("/api/v1/rentals/all/1")
    assert response.status_code == 401
    assert response.json()["detail"] == "Requires authentication"


def test_get_rental_authorized_without_permissions(
    client_with_customer_auth,
    multiple_rentals,
):
    """Test accessing rental_id endpoint without permissions returns 403."""
    response = client_with_customer_auth.get("/api/v1/rentals/all/1")
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission 'read:rentals' required"


def test_get_rental_authorized_with_permissions(
    client_with_staff_auth,
    multiple_rentals,
):
    """Test accessing rental_id endpoint with permissions returns 200."""
    response = client_with_staff_auth.get("/api/v1/rentals/all/1")
    assert response.status_code == 200
    rental = response.json()
    assert rental is not None
    assert rental["rental_id"] == multiple_rentals[0].rental_id
    assert rental["customer_id"] == multiple_rentals[0].customer_id
    assert rental["inventory_id"] == multiple_rentals[0].inventory_id


def test_return_rental_unauthorized(client):
    """Test accessing protected endpoint without auth returns 401."""
    response = client.patch("/api/v1/rentals/1/return")
    assert response.status_code == 401
    assert response.json()["detail"] == "Requires authentication"


def test_return_rental_authorized_without_permissions(client_with_customer_auth):
    """Test accessing protected endpoint without permissions returns 403."""
    response = client_with_customer_auth.patch("/api/v1/rentals/1/return")
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission 'write:rentals' required"


def test_return_rental_authorized_with_permissions(
    client_with_staff_auth,
    multiple_rentals,
):
    """Test accessing protected endpoint without auth returns 200."""
    # Rental with id 3 is not returned
    response = client_with_staff_auth.patch("/api/v1/rentals/3/return")
    assert response.status_code == 200
    # Rental with id 1 is already returned
    response = client_with_staff_auth.patch("/api/v1/rentals/1/return")
    assert response.status_code == 405
