from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")

engine_options = {}
if DATABASE_URL.startswith("sqlite"):
    engine_options = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool
    }

engine = create_engine(DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()