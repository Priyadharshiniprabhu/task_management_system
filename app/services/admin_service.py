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

    # Validate Project
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

    # Validate User
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

    # Check if user is already mapped to ANY project
        existing_user_mapping = (
            db.query(UserProject)
            .filter(
                UserProject.user_id == request.user_id
            )
            .first()
        )

        if existing_user_mapping:
            raise HTTPException(
                status_code=400,
                detail="The user has already mapped with another project"
            )

    # Check duplicate mapping
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
        db.refresh(mapping)

        return {
            "message": "User mapped successfully",
            "user_id": request.user_id,
            "project_id": request.project_id
        }

    @staticmethod
    def get_all_users_by_project(db):

        projects = db.query(Project).filter(
            Project.is_active == True
        ).all()

        response = {}

        for project in projects:

            mappings = (
                db.query(UserProject)
                .filter(
                    UserProject.project_id == project.id
                )
                .all()
            )

            users = []

            for mapping in mappings:

                user = (
                    db.query(User)
                    .filter(
                        User.id == mapping.user_id,
                        User.is_active == True
                    )
                    .first()
                )

                if user:

                    users.append({
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    })

            response[project.project_name] = {
                "users": users
            }

        return response

    @staticmethod
    def create_project(request, db):
    
            existing_project = (
                db.query(Project)
                .filter(
                    Project.project_name == request.project_name,
                    Project.is_active == True
                )
                .first()
            )
    
            if existing_project:
                raise HTTPException(
                    status_code=400,
                    detail="Project already exists"
                )
    
            project = Project(
                project_name=request.project_name,
                description=request.description,
                is_active=True
            )
    
            db.add(project)
            db.commit()
            db.refresh(project)
    
            return {
                "message": "Project created successfully",
                "project_id": project.id
            }
    
