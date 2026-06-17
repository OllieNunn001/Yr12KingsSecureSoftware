import pytest
from app import app
from database.data import clear_database

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear():
    clear_database()

def test_successful_logout(client):
    """Test successful logout"""
    response = client.post(
        "/admin/auth/register",
        json={
            "email": "mmadrid@kings.edu.au",
            "password": "StrongPass1!",
            "name": "Martin Madrid",
        },
    )

    assert response.status_code == 200
    session_token = response.get_json()["session_token"]
    # TODO: Test CSRF token retrieval and inclusion
    csrf_token = response.get_json().get("csrf_token")

    response = client.post(
        "/admin/auth/logout",
        headers={
            "Authorization": session_token,
            "X-CSRF-Token": csrf_token
        }
    )

    assert response.status_code == 200
    assert response.get_json() == {}


def test_invalid_tokens_logout(client):
    """Test invalid token"""
    # TODO: Test with invalid session and CSRF tokens
    response1 = client.post(
        "/admin/auth/logout",
        headers={
            "Authorization": "Invalid token",
            # TODO: Include invalid X-CSRF-Token header
            "X-CSRF-Token": "Invalid CSRF token"
        },
    )

    assert response1.status_code == 403


def test_missing_tokens(client):
    """Test missing tokens in request"""
    # TODO: Test missing CSRF token validation
    response = client.post("/admin/auth/logout")
    assert response.status_code == 403
