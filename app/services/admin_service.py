from fastapi import HTTPException

from app.models import User
from app.models import Project
from app.models import UserProject


class AdminService:

    @staticmethod
    def map_user_to_project(
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

        existing_mapping = (
            db.query(UserProject)
            .filter(
                UserProject.user_id == request.user_id,
                UserProject.project_id == request.project_id
            )
            .first()
        )

        if existing_mapping:
            raise HTTPException(
                status_code=400,
                detail="User already mapped to project"
            )

        mapping = UserProject(
            user_id=request.user_id,
            project_id=request.project_id
        )

        db.add(mapping)
        db.commit()

        return {
            "message":
            "User mapped successfully"
        }