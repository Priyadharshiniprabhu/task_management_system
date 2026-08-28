from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.logger_config import logger

from app.schemas import RegisterRequest
from app.schemas import LoginRequest

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
        request: RegisterRequest,
        db: Session = Depends(get_db)
):

    try:

        user = AuthService.register(
            request,
            db
        )

        return {
            "message":
            "User registered successfully",
            "user_id":
            user.id
        }

    except Exception as e:

        logger.error(f"Error while creating admin user: {str(e)}")

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
        request: LoginRequest,
        db: Session = Depends(get_db)
):

    response = AuthService.login(
        request,
        db
    )

    if not response:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return response