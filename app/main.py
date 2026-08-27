from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.routers.auth_router import router
from app.routers.admin_router import router as admin_router
from app.routers.task_router import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API"
)

# user
app.include_router(router)

# admin
app.include_router(admin_router)

# tasks
app.include_router(task_router)