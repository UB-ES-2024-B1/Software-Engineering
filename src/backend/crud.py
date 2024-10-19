# backend/crud.py

from sqlalchemy.orm import Session
from . import models

def create_user(db: Session, name: str, email: str):

    db_user = models.User(name=name, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
