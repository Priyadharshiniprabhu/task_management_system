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

    @staticmethod
    def get_all_tasks(db):

        tasks = (
            db.query(Task)
            .filter(
                Task.is_active == True,
                Task.status != "VERIFIED_COMPLETED"
            )
            .all()
        )

        response = []

        for task in tasks:
 
            user = (
                db.query(User)
                .filter(
                    User.id == task.user_id
                )
                .first()
            )

            response.append(
                {
                    "task_id": task.id,
                    "task_name": task.task_name,
                    "description": task.description,
                    "priority": task.priority,
                    "status": task.status,
                    "assigned_user": user.username
                }
            )
        return response

    @staticmethod
    def get_user_tasks(
            current_user,
            db
    ):
  
        tasks = (
            db.query(Task)
            .filter(
                Task.user_id == current_user.id,
                Task.is_active == True,
                Task.status != "VERIFIED_COMPLETED"
            )
            .all()
        )

        response = []

        for task in tasks:
  
            response.append(
                {
                    "task_id": task.id,
                    "task_name": task.task_name,
                    "description": task.description,
                    "priority": task.priority,
                    "status": task.status
                }
            )

        return response

    @staticmethod
    def update_task_status(
            task_id,
            request,
            current_user,
            db
    ):

        task = (
            db.query(Task)
            .filter(
                Task.id == task_id,
                Task.is_active == True
            )
            .first()
        )

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        if task.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to update this task"
            )

        valid_statuses = [
            "IN_PROGRESS",
            "COMPLETED_BY_USER"
        ]

        if request.status.upper() not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail="Invalid status"
            )

        if (
                task.status == "ASSIGNED"
                and request.status.upper() == "COMPLETED_BY_USER"
        ):
            raise HTTPException(
                status_code=400,
                detail="Task must be moved to IN_PROGRESS first"
            )

        if (
                task.status == "COMPLETED_BY_USER"
        ):
            raise HTTPException(
                status_code=400,
                detail="Task already submitted for review"
            )

        task.status = request.status.upper()

        db.commit()
        db.refresh(task)

        return {
            "message": "Task status updated successfully",
            "task_id": task.id,
            "status": task.status
        }

    @staticmethod
    def get_tasks_for_review(db):

        tasks = (
            db.query(Task)
            .filter(
                Task.is_active == True,
                Task.status == "COMPLETED_BY_USER"
            )
            .all()
        )

        response = []

        for task in tasks:
  
            user = (
                db.query(User)
                .filter(User.id == task.user_id)
                .first()
            )

            project = (
                db.query(Project)
                .filter(Project.id == task.project_id)
                .first()
            )

            response.append(
                {
                    "task_id": task.id,
                    "task_name": task.task_name,
                    "priority": task.priority,
                    "status": task.status,
                    "assigned_user": user.username,
                    "project_name": project.project_name
                }
            )

        return response

    @staticmethod
    def verify_task(
            task_id,
            db
    ):

        task = (
            db.query(Task)
            .filter(
                Task.id == task_id,
                Task.is_active == True
            )
            .first()
        )

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        if task.status != "COMPLETED_BY_USER":
            raise HTTPException(
                status_code=400,
                detail="Only completed tasks can be verified"
            )

        task.status = "VERIFIED_COMPLETED"

        db.commit()
        db.refresh(task)

        return {
            "message": "Task verified successfully",
            "task_id": task.id,
            "status": task.status
        }

    @staticmethod
    def delete_task(task_id, db):

        task = (
            db.query(Task)
            .filter(
                Task.id == task_id,
                Task.is_active == True
            )
            .first()
        )

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        task.is_active = False
        db.commit()

        return {
            "message": "Task deleted successfully"
        }