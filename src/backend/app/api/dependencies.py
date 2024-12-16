# backend/app/api/dependencies.py
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import authenticate_user
from app.core.jwt import decode_token
from app.crud import user_crud
from app.models import User
from typing import Generator  # Import Generator from typing
from app.db.database import SessionLocal
from app.api.db_utils import get_db

# Configuración de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

# Obtener usuario actual usando el token JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    email = decode_token(token)
    user = user_crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def is_admin(user: User = Depends(get_current_user)) -> User:
    """
    Check if the current user is an admin.
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this resource",
        )
    return user