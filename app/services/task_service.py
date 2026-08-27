from fastapi import HTTPException

from app.models import User
from app.models import Project
from app.models import UserProject
from app.models import Task


class TaskService:

    @staticmethod
    def create_task(
            request,
            db
    ):

        project = (
            db.query(Project)
            .filter(
                Project.id == request.project_id,
                Project.is_active == True
            )
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        user = (
            db.query(User)
            .filter(
                User.id == request.user_id,
                User.is_active == True
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        mapping = (
            db.query(UserProject)
            .filter(
                UserProject.user_id == request.user_id,
                UserProject.project_id == request.project_id
            )
            .first()
        )

        if not mapping:
            raise HTTPException(
                status_code=400,
                detail="User is not mapped to this project"
            )

        valid_priorities = [
            "HIGH",
            "MEDIUM",
            "LOW"
        ]

        if request.priority.upper() not in valid_priorities:
            raise HTTPException(
                status_code=400,
                detail="Invalid priority"
            )

        task = Task(
            task_name=request.task_name,
            description=request.description,
            priority=request.priority.upper(),
            status="ASSIGNED",
            user_id=request.user_id,
            project_id=request.project_id,
            is_active=True
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "message": "Task created successfully",
            "task_id": task.id
        }