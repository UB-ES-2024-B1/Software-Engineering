from passlib.context import CryptContext
from app.models import User
from sqlalchemy.orm import Session
from app.crud import user_crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Cifrar contraseña
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Autenticación de usuario
def authenticate_user(db: Session, email: str, password: str) -> User | bool:
    user = user_crud.get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user
