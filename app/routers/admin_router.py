from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from app.schemas import UserProjectMappingRequest

from app.database import get_db
from app.services.admin_service import AdminService
from app.dependencies import admin_required
from app.models import Project
from app.schemas import CreateProjectRequest

router = APIRouter(prefix="/admin", tags=["Admin"])

class AdminService:
    @staticmethod
    def get_all_users_by_project(db):

        projects = db.query(Project).all()
        response = {}
        for project in projects:
            response[project.project_name] = {
                "users": [
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
                    for user in project.users
                ]
            }

        return response

@router.get("/users")
def get_all_users(db: Session = Depends(get_db), current_user=Depends(admin_required)):
    return AdminService.get_all_users_by_project(db)

@router.post("/project-user-mapping")
def map_user_to_project(request: UserProjectMappingRequest, db: Session = Depends(get_db), current_user=Depends(admin_required)):
    return AdminService.map_user_to_project(request, db)

@router.post("/projects")
def create_project(request: CreateProjectRequest, db: Session = Depends(get_db), current_user=Depends(admin_required)):
    return AdminService.create_project(request, db)