from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task(admin_token):

    response = client.post(
        "/admin/tasks",
        json={
            "task_name": "Develop Login API",
            "description": "Implement JWT",
            "priority": "HIGH",
            "user_id": 2,
            "project_id": 1
        },
        headers={
            "Authorization":
            f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "task_id" in data

def test_get_all_tasks(admin_token):

    response = client.get(
        "/admin/tasks",
        headers={
            "Authorization":
            f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

def test_get_user_tasks(user_token):

    response = client.get(
        "/user/tasks",
        headers={
            "Authorization":
            f"Bearer {user_token}"
        }
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

