from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_delete_task(
        admin_token
):

    response = client.delete(
        "/admin/tasks/1",
        headers={
            "Authorization":
            f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == \
           "Task deleted successfully"

def test_invalid_login():

    response = client.post(
        "/auth/login",
        json={
            "email":"wrong@gmail.com",
            "password":"Wrong123"
        }
    )

    assert response.status_code == 401

def test_project_creation_by_user(
        user_token
):

    response = client.post(
        "/admin/projects",
        json={
            "project_name":"Test",
            "description":"Test"
        },
        headers={
            "Authorization":
            f"Bearer {user_token}"
        }
    )

    assert response.status_code == 403

def test_duplicate_mapping(
        admin_token
):

    response = client.post(
        "/admin/project-user-mapping",
        json={
            "project_id":1,
            "user_id":2
        },
        headers={
            "Authorization":
            f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 400

