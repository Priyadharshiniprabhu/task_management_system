from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.services.task_service import TaskService
from app.schemas import UpdateTaskStatusRequest


router = APIRouter(prefix="/user", tags=["User"])


@router.get("/tasks")
def get_user_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    return TaskService.get_user_tasks(current_user, db)

@router.patch("/tasks/{task_id}")
def update_task_status(task_id: int, request: UpdateTaskStatusRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    return TaskService.update_task_status(task_id, request, current_user, db)
