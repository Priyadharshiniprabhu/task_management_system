from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from app.schemas import UserProjectMappingRequest

from app.database import get_db
from app.services.admin_service import AdminService
from app.dependencies import admin_required

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
def get_all_users(db: Session = Depends(get_db), current_user=Depends(admin_required)):

    return AdminService.get_all_users_by_project(
        db
    )

@router.post("/project-user-mapping")
def map_user_to_project(request: UserProjectMappingRequest, db: Session = Depends(get_db), current_user=Depends(admin_required)):
    return AdminService.map_user_to_project(request, db)