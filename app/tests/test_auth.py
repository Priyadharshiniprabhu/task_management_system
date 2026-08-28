from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():

    response = client.post(
        "/auth/register",
        json={
            "username": "Priya",
            "email": "priya@gmail.com",
            "password": "Priya123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "user_id" in data


def test_login():

    response = client.post(
        "/auth/login",
        json={
            "email": "priya@gmail.com",
            "password": "Priya123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "Bearer"