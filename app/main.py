from fastapi import FastAPI
from fastapi import Request

from app.database import Base
from app.database import engine

from app.routers.auth_router import router
from app.routers.admin_router import router as admin_router
from app.routers.task_router import router as task_router
from app.routers.user_router import router as user_router
from app.logger_config import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API"
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(
        "%s %s %s",
        request.method,
        request.url.path,
        response.status_code
    )
    return response

# auth
app.include_router(router)

# admin
app.include_router(admin_router)

# tasks
app.include_router(task_router)

# user
app.include_router(user_router)
