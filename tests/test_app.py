"""Test the app module."""

from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_public_success():
    """Test public endpoint."""
    response = client.get("/api/public")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_private_without_authentication():
    """Test private endpoint without authentication."""
    response = client.get("/api/private")
    assert response.status_code == 401
    assert response.json()["detail"] == "Requires authentication"
