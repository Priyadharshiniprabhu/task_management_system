from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_update_task_to_in_progress(
        user_token
):

    response = client.patch(
        "/user/tasks/1",
        json={
            "status":
            "IN_PROGRESS"
        },
        headers={
            "Authorization":
            f"Bearer {user_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == \
           "IN_PROGRESS"

def test_complete_task(
        user_token
):

    response = client.patch(
        "/user/tasks/1",
        json={
            "status":
            "COMPLETED_BY_USER"
        },
        headers={
            "Authorization":
            f"Bearer {user_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == \
           "COMPLETED_BY_USER"

def test_review_queue(
        admin_token
):

    response = client.get(
        "/admin/tasks/review",
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

def test_verify_task(
        admin_token
):

    response = client.patch(
        "/admin/tasks/1/verify",
        headers={
            "Authorization":
            f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == \
           "VERIFIED_COMPLETED"

