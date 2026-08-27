from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import admin_required
from app.schemas import CreateTaskRequest
from app.services.task_service import TaskService


router = APIRouter(
    prefix="/admin/tasks",
    tags=["Task Management"]
)


@router.post("")
def create_task(
        request: CreateTaskRequest,
        db: Session = Depends(get_db),
        current_user=Depends(admin_required)
):

    return TaskService.create_task(
        request,
        db
    )