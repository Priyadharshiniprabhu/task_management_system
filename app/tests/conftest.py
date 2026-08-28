import os

os.environ["DATABASE_URL"] = "sqlite://"

import pytest

from fastapi.testclient import TestClient
from app.main import app
from app.auth import hash_password
from app.database import SessionLocal
from app.database import Base
from app.database import engine
from app.models import Project, Task, User

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def seed_test_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(Task).delete()
    db.query(Project).delete()
    db.query(User).delete()
    db.add_all([
        User(
            username="Admin",
            email="admin@gmail.com",
            password=hash_password("Admin@123"),
            role="ADMIN",
            is_active=True
        ),
        User(
            username="John",
            email="john@gmail.com",
            password=hash_password("John123"),
            role="USER",
            is_active=True
        )
    ])
    db.commit()

    db.add(Project(
        project_name="Initial Project",
        description="Test project",
        is_active=True
    ))
    db.commit()

    db.add(Task(
        task_name="Initial Task",
        description="Test task",
        priority="HIGH",
        status="ASSIGNED",
        user_id=2,
        project_id=1,
        is_active=True
    ))
    db.commit()
    db.close()

    yield

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
