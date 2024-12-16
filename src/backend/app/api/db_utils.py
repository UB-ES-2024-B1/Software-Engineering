# app/api/db_utils.py
from sqlalchemy.orm import Session
from app.db.database import SessionLocal  # Adjust to your structure

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()