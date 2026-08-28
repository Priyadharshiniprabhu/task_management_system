# create_admin.py

from getpass import getpass
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.auth import hash_password

from app.logger_config import logger


def create_admin():

    db: Session = SessionLocal()

    try:
        print("\n===== CREATE ADMIN USER =====\n")

        username = input("Enter Admin Name: ")

        email = input("Enter Admin Email: ")

        password = getpass("Enter Admin Password: ")

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            print("\nAdmin/User already exists with this email.")
            return

        admin_user = User(
            username=username,
            email=email,
            password=hash_password(password),
            role="ADMIN",
            is_active=True
        )

        db.add(admin_user)
        db.commit()

        print("\nAdmin created successfully.")
        print(f"Email : {email}")
        print("Role  : ADMIN")

    except Exception as e:
        db.rollback()
        logger.error(f"Admin creation failed!: {str(e)}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()