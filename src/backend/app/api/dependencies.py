# backend/app/api/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator  # Import Generator from typing
from app.db.database import SessionLocal

# Dependency to get a new database session for each request
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()  # Open a new session
    try:
        yield db  # Yield the session to be used by the route handler
    finally:
        db.close()  # Ensure the session is closed after the request is done