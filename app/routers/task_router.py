from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import admin_required
from app.schemas import CreateTaskRequest
from app.services.task_service import TaskService
from app.auth import get_current_user

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

@router.get("")
def get_all_tasks(
        db: Session = Depends(get_db),
        current_user=Depends(admin_required)
):

    return TaskService.get_all_tasks(
        db
    )

@router.get("/review")
def get_tasks_for_review(
        db: Session = Depends(get_db),
        current_user=Depends(admin_required)
):

    return TaskService.get_tasks_for_review(db)

@router.patch("/{task_id}/verify")
def verify_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(admin_required)
):

    return TaskService.verify_task(
        task_id,
        db
    )