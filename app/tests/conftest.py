import pytest

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def admin_token():

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "Admin@123"
        }
    )

    return response.json()["access_token"]


@pytest.fixture
def user_token():

    response = client.post(
        "/auth/login",
        json={
            "email": "john@gmail.com",
            "password": "John123"
        }
    )

    return response.json()["access_token"]