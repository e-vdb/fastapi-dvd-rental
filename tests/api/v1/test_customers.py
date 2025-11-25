"""Test suite for the customers router of the api."""


def test_get_customer_unauthorized(client):
    """Test accessing protected endpoint without auth returns 401."""
    response = client.get("/api/v1/customers/1")
    assert response.status_code == 401
    assert response.json()["detail"] == "Requires authentication"


def test_get_customer_authorized_without_permissions(client_with_customer_auth):
    """Test accessing customer_id endpoint without permissions returns 403."""
    response = client_with_customer_auth.get("/api/v1/customers/1")
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission 'read:customers' required"


def test_get_customer_authorized_with_permissions(
    client_with_staff_auth,
    sample_customer,
):
    """Test accessing customer_id endpoint with correct permissions returns 200."""
    response = client_with_staff_auth.get("/api/v1/customers/1")
    assert response.status_code == 200
    customer = response.json()
    assert customer is not None
    assert customer["customer_id"] == sample_customer.customer_id
    assert customer["first_name"] == sample_customer.first_name
    assert customer["last_name"] == sample_customer.last_name


def test_get_customer_rentals_unauthorized(client):
    """Test accessing protected endpoint without auth returns 401."""
    response = client.get("/api/v1/customers/1/rentals")
    assert response.status_code == 401
    assert response.json()["detail"] == "Requires authentication"


def test_get_customer_rentals_authorized_without_permissions(client_with_customer_auth):
    """Test accessing customer_id endpoint without permissions returns 403."""
    response = client_with_customer_auth.get("/api/v1/customers/1/rentals")
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission 'read:rentals' required"


def test_get_customer_rentals_authorized_with_permissions(
    client_with_staff_auth,
    customer_with_rentals,
):
    """Test accessing customer_id endpoint with permissions returns 200."""
    response = client_with_staff_auth.get("/api/v1/customers/1/rentals")
    assert response.status_code == 200
    rentals = response.json()
    assert rentals is not None
    assert len(rentals) == 3
    assert rentals[0]["title"] == "The Shawshank Redemption"
