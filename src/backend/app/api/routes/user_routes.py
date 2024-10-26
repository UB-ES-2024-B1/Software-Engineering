# backend/app/api/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal  # Import the SessionLocal from database.py
from app.crud import user_crud
from app.api.dependencies import get_db  # Import the get_db function
from app.models import (
    User, UserOut, UserCreate, Message, UserUpdate
)
from typing import List

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
            {"email": "user1@example.com", "is_admin": True, "full_name": "User1", "password": "password1"},
            {"email": "user2@example.com", "is_admin": True, "full_name": "User2", "password": "password2"},
            {"email": "user3@example.com", "is_admin": True, "full_name": "User3", "password": "password3"},
            {"email": "user4@example.com", "is_admin": True, "full_name": "User4", "password": "password4"},
            {"email": "user5@example.com", "is_admin": True, "full_name": "User5", "password": "password5"},
            {"email": "user6@example.com", "is_admin": True, "full_name": "User6", "password": "password6"},
        ]
        # Insertar usuarios en la base de datos
        for user_data in initial_users:
            user_crud.create_user(
                db=db,
                full_name=user_data.get("full_name"),
                email=user_data.get("email"),
                hashed_password=pwd_context.hash(user_data.get("password")),
                is_admin=user_data.get("is_admin")
            )
    db.close()  # Close session

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
@router.get("/{user_id}", response_model=UserOut)
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

# Route to delete a user by ID
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)) -> Message:
    """
    Delete a user by their ID.
    :param user_id: The ID of the user to delete
    :param db: Database session (injected via dependency)
    :return: The deleted user object
    """
    user = user_crud.delete_user(db, user_id=user_id)
    if user is False:
        raise HTTPException(status_code=404, detail="User not found")
    return Message(id=user_id)

# Endpoint to update an existing user by ID
@router.put("/id/{user_id}", response_model=UserOut)
def update_user_by_id(
    user_id: int,
    user_data: UserUpdate,  # Model with the data to update
    db: Session = Depends(get_db)
):
    """
    Update an existing user by ID.
    :param user_id: The ID of the user to update
    :param user_data: The data to update the user
    :param db: The database session
    :return: The updated user
    """
    # Use the CRUD function to update the user
    updated_user = user_crud.update_user(db, user_id, user_data.model_dump(exclude_unset=True))

    # If the user doesn't exist, return error 404
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user

# Endpoint to update an existing user by email
@router.put("/email/{user_email}", response_model=UserOut)
def update_user_by_email(
    user_email: str,  # The user's email to identify the user
    user_data: UserUpdate,  # Model with the data to update
    db: Session = Depends(get_db)
):
    """
    Update an existing user by email.
    :param user_email: The email of the user to update
    :param user_data: The data to update the user
    :param db: The database session
    :return: The updated user
    """
    # Use the CRUD function to update the user by email
    updated_user = user_crud.update_user_by_email(db, user_email, user_data.model_dump(exclude_unset=True))

    # If the user doesn't exist, return error 404
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user
