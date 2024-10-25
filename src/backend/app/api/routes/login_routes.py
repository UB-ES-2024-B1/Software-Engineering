from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.jwt import create_access_token, decode_token
from app.core.security import get_password_hash, authenticate_user
from app.core.jwt import ACCESS_TOKEN_EXPIRE_MINUTES
from app.api.dependencies import get_current_user
from .user_routes import get_db
from app.models.user_models import User, TokenRequest

from app.crud import user_crud

router = APIRouter()

@router.post("/")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)  # Solo usar la sesión como dependencia
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta protegida para obtener el usuario actual
@router.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/test-token")
def test_token(token_request: TokenRequest, db: Session = Depends(get_db)):
    """
    Verifica si el token es válido.
    Devuelve información del usuario actual si es válido.
    """
    email = decode_token(token_request.token)  # Decodifica el token
    user = user_crud.get_user_by_email(db, email=email)  # Obtiene el usuario por email
    
    if user is None:
        raise HTTPException(status_code=401, detail="Token is invalid or user not found")
    
    return {"message": "Token is valid", "user": user}

'''
@router.post("/recover-password/")
def recover_password(email: str, db: Session = Depends(get_db)):
    """
    Envía un correo electrónico para recuperar la contraseña.
    Se supone que el correo electrónico contendrá un enlace para restablecer la contraseña.
    """
    user = user_crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Aquí se puede implementar la lógica para enviar un correo.
    
    return {"message": "Recovery email sent"}

'''
@router.post("/reset-password/")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    """
    Restablece la contraseña del usuario.
    El token debe ser válido y estar asociado al usuario.
    """
    email = decode_token(token)  # Asegúrate de que este token sea el adecuado para restablecimiento
    user = user_crud.get_user_by_email(db, email=email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    # Hashea la nueva contraseña
    hashed_password = get_password_hash(new_password)
    
    # Actualiza la contraseña del usuario
    user.hashed_password = hashed_password
    
    # Guarda los cambios en la base de datos
    db.commit()

    return {"message": "Password has been reset successfully"}
