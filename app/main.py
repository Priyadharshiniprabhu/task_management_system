from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.routers.auth_router import router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API"
)

app.include_router(router)