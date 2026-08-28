from sqlalchemy.orm import Session

from app.models import User
from app.auth import hash_password
from app.auth import verify_password
from app.auth import create_access_token

from app.logger_config import logger

class AuthService:

    @staticmethod
    def register(
            register_request,
            db: Session
    ):

        existing_user = db.query(User).filter(
            User.email == register_request.email
        ).first()

        if existing_user:
            raise Exception(
                "Email already registered"
            )

        user = User(
            username=register_request.username,
            email=register_request.email,
            password=hash_password(
                register_request.password
            ),
            role="USER"
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(f"New user registered: {user.email}")

        return user

    @staticmethod
    def login(
            login_request,
            db: Session
    ):

        user = db.query(User).filter(
            User.email == login_request.email
        ).first()

        if not user:
            return None

        password_valid = verify_password(
            login_request.password,
            user.password
        )

        if not password_valid:
            return None

        token = create_access_token(
            {
                "sub": user.email,
                "role": user.role
            }
        )

        logger.info(f"User logged in: {user.email}")

        return {
            "access_token": token,
            "token_type": "Bearer",
            "role": user.role
        }