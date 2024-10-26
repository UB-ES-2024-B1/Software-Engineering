from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import authenticate_user
from app.core.jwt import decode_token
from app.crud import user_crud
from app.models import User
from app.api.routes import user_routes

# Configuración de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

# Obtener usuario actual usando el token JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(user_routes.get_db)) -> User:
    email = decode_token(token)
    user = user_crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

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

