# backend/app/api/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.database import SessionLocal  # Import the SessionLocal from database.py
from app.crud import user_crud
from app.api.dependencies import *  # Import the get_db function
from app.models import (
    User, UserOut, UserCreate,UserUpdate
)
from scripts.upload import eliminar_imagen, subir_imagen_desde_archivo
from typing import List, Optional

router = APIRouter()

# Instance of CryptContext for hash the password
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_db():
    # Consumir el generador para obtener la sesión
    db: Session = next(get_db())  # Obtener una sesión válida

    # Verificar si ya existen usuarios
    if len(user_crud.get_users(db)) == 0:
        # Crear 6 usuarios
        initial_users = [
            {"email": "user1@example.com", "is_admin": True, "full_name": "User1", "password": "password1", "img_url": "https://res.cloudinary.com/dt2flsyai/image/upload/v1732536167/imagenes-perfil/profile-circle.svg", "img_public_id": "imagenes-perfil/profile-circle", "is_premiun": True},
            {"email": "user2@example.com", "is_admin": True, "full_name": "User2", "password": "password2", "img_url": "https://res.cloudinary.com/dt2flsyai/image/upload/v1732536167/imagenes-perfil/profile-circle.svg", "img_public_id": "imagenes-perfil/profile-circle", "is_premiun": True},
            {"email": "user3@example.com", "is_admin": True, "full_name": "User3", "password": "password3", "img_url": "https://res.cloudinary.com/dt2flsyai/image/upload/v1732536167/imagenes-perfil/profile-circle.svg", "img_public_id": "imagenes-perfil/profile-circle", "is_premiun": True},
            {"email": "user4@example.com", "is_admin": True, "full_name": "User4", "password": "password4", "img_url": "https://res.cloudinary.com/dt2flsyai/image/upload/v1732536167/imagenes-perfil/profile-circle.svg", "img_public_id": "imagenes-perfil/profile-circle", "is_premiun": True},
            {"email": "user5@example.com", "is_admin": True, "full_name": "User5", "password": "password5", "img_url": "https://res.cloudinary.com/dt2flsyai/image/upload/v1732536167/imagenes-perfil/profile-circle.svg", "img_public_id": "imagenes-perfil/profile-circle", "is_premiun": False},
            {"email": "user6@example.com", "is_admin": True, "full_name": "User6", "password": "password6", "img_url": "https://res.cloudinary.com/dt2flsyai/image/upload/v1732536167/imagenes-perfil/profile-circle.svg", "img_public_id": "imagenes-perfil/profile-circle", "is_premiun": False},
        ]
        # Insertar usuarios en la base de datos
        for user_data in initial_users:
            user_crud.create_user(
                db=db,
                full_name=user_data.get("full_name"),
                email=user_data.get("email"),
                hashed_password=pwd_context.hash(user_data.get("password")),
                is_admin=user_data.get("is_admin")
                #is_premium=user_data.get("is_premium")
            )
    db.close()  # Cerrar la sesión
    
# Route to create a new user
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    :param user: UserCreate (input validation)
    :param db: Database session (injected via dependency)
    :return: The created user object
    """
    # Check if the email is already registered
    existing_user = user_crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Call the CRUD operation to create the user in the database
    new_user = user_crud.create_user(db, full_name=user.full_name, email=user.email, hashed_password=hashed_password)
    return new_user

# Route to get all users
@router.get("/", response_model=List[UserOut])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of users.
    :param skip: Pagination offset
    :param limit: Pagination limit
    :param db: Database session (injected via dependency)
    :return: A list of users
    """
    # Fetch the list of users with pagination
    users = user_crud.get_users(db, skip=skip, limit=limit)

    # Return the list of users
    return users

# Route to get a user by ID
@router.get("/id/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by their ID.
    :param user_id: The ID of the user
    :param db: Database session (injected via dependency)
    :return: User object or 404 if not found
    """
    user = user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/email/{user_email}", response_model=UserOut)
def read_user_mail(user_email: str, db: Session = Depends(get_db)):
    """
    Get a user by their ID.
    :param user_id: The ID of the user
    :param db: Database session (injected via dependency)
    :return: User object or 404 if not found
    """
    user = user_crud.get_user_by_email(db, user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Route to delete a user by ID
@router.delete("/id/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.
    :param user_id: The ID of the user to delete
    :param db: Database session (injected via dependency)
    :return: The deleted user object
    """
    user = user_crud.delete_user(db, user_id=user_id)
    if user is False:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted succesfully"}

# Route to delete a user by email
@router.delete("/email/{user_email}")
def delete_user_mail(user_email: str, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.
    :param user_id: The ID of the user to delete
    :param db: Database session (injected via dependency)
    :return: The deleted user object
    """
    user = user_crud.delete_user_by_email(db, user_email=user_email)
    if user is False:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted succesfully"}

# Endpoint to update an existing user by ID
@router.put("/id/{user_id}", response_model=UserOut)
def update_user_by_id(
    user_id: int,
    email: Optional[str] = Form(None),
    full_name: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    is_admin: Optional[bool] = Form(None),
    img: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Update an existing user by ID.
    :param user_id: The ID of the user to update
    :param email: The new email, if provided
    :param full_name: The new full name, if provided
    :param is_active: Whether the user is active, if provided
    :param is_admin: Whether the user is an admin, if provided
    :param img_url: The URL of the image, if provided
    :param img_public_id: The public ID of the image, if provided
    :param img: The uploaded image, if provided
    :param db: The database session
    :return: The updated user
    """
    
    # Get the current user from the database
    existing_user = user_crud.get_user(db, user_id)
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare the data for updating
    update_data = {}
    if email is not None:
        update_data["email"] = email
    if full_name is not None:
        update_data["full_name"] = full_name
    if is_active is not None:
        update_data["is_active"] = is_active
    if is_admin is not None:
        update_data["is_admin"] = is_admin


    # If an image is uploaded, process it
    if img:
        try:
            if existing_user.img_public_id and existing_user.img_public_id != "imagenes-perfil/profile-circle":
                # If there is an existing image, delete it from Cloudinary
                eliminar_imagen(existing_user.img_public_id)

            # Upload the new image and update the fields
            image_data = img.file.read()  # Read the image bytes
            upload_result = subir_imagen_desde_archivo(image_data)  # Call the upload function
            
            update_data["img_url"] = upload_result["url"]
            update_data["img_public_id"] = upload_result["public_id"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")
    
    # Update the user with the new data
    updated_user = user_crud.update_user(db, user_id, update_data)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user

@router.put("/email/{user_email}", response_model=UserOut)
def update_user_by_email(
    user_email: str,
    email: Optional[str] = Form(None),
    full_name: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    is_admin: Optional[bool] = Form(None),
    img: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Update an existing user by email.
    :param user_email: The email of the user to update
    :param email: The new email, if provided
    :param full_name: The new full name, if provided
    :param is_active: Whether the user is active, if provided
    :param is_admin: Whether the user is an admin, if provided
    :param img: The uploaded image, if provided
    :param db: The database session
    :return: The updated user
    """
    # Get the current user from the database
    existing_user = user_crud.get_user_by_email(db, user_email)
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare the data for updating
    update_data = {}
    if email is not None:
        update_data["email"] = email
    if full_name is not None:
        update_data["full_name"] = full_name
    if is_active is not None:
        update_data["is_active"] = is_active
    if is_admin is not None:
        update_data["is_admin"] = is_admin

    # If an image is uploaded, process it
    if img:
        try:
            if existing_user.img_public_id and existing_user.img_public_id != "imagenes-perfil/profile-circle":
                # If there is an existing image, delete it from Cloudinary
                eliminar_imagen(existing_user.img_public_id)

            # Upload the new image and update the fields
            image_data = img.file.read()  # Read the image bytes
            upload_result = subir_imagen_desde_archivo(image_data)  # Call the upload function
            
            update_data["img_url"] = upload_result["url"]
            update_data["img_public_id"] = upload_result["public_id"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")
    
    # Update the user with the new data
    updated_user = user_crud.update_user(db, existing_user.id, update_data)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")   
    return updated_user

def is_admin_user(current_user: User = Depends(get_current_user)) -> bool:
    """
    Verifica si el usuario actual es administrador.
    
    :param current_user: User - El usuario actual autenticado
    :return: bool - True si el usuario es administrador, False de lo contrario
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permission to do this action."
        )
    return True

# Endpoint to upgrade a user to premium
@router.put("/upgrade_premium/{user_email}", response_model=UserOut)
def upgrade_user_to_premium(user_email: str, db: Session = Depends(get_db)):
    """
    Upgrade a user to premium by email.

    :param user_email: email of the current user
    """
    user = user_crud.upgrade_to_premium_by_email(db, user_email=user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint to downgrade a user to premium
@router.put("/downgrade_premium/{user_email}", response_model=UserOut)
def downgrade_user_to_premium(user_email: str, db: Session = Depends(get_db)):
    """
    Downgrade a user to premium by email.

    :param user_email: email of the current user
    """
    user = user_crud.downgrade_to_premium_by_email(db, user_email=user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user