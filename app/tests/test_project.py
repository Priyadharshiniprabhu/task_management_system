from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_project(admin_token):

    response = client.post(
        "/admin/projects",
        json={
            "project_name": "Banking Project",
            "description": "Demo Project"
        },
        headers={
            "Authorization":
            f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "project_id" in data


def test_project_user_mapping(admin_token):

    response = client.post(
        "/admin/project-user-mapping",
        json={
            "project_id": 1,
            "user_id": 2
        },
        headers={
            "Authorization":
            f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == \
           "User mapped successfully"