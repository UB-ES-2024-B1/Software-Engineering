# backend/app/crud/user_crud.py
from sqlalchemy.orm import Session
from app.models.user_models import User, UserOut

# Function to create a user
def create_user(db: Session, full_name: str, email: str, hashed_password: str) -> UserOut:
    db_user = User(full_name=full_name, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetch a list of users from the database with pagination.
    :param db: Database session
    :param skip: Number of records to skip
    :param limit: Number of records to return
    :return: List of User objects
    """
    return db.query(User).offset(skip).limit(limit).all()

# Function that obtein a user by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# CRUD method to get a user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Function to delete a user by ID
def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user from the database by their ID.
    :param db: The database session
    :param user_id: The ID of the user to be deleted
    :return: True if the user was deleted, False if not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True  # Deletion successful
    return False  # User not found

def update_user(db: Session, user_id: int, user_data: dict):
    """
    Update an existing user in the database by ID.
    :param db: Database session
    :param user_id: The ID of the user to update
    :param user_data: Dictionary of fields to update
    :return: Updated User object
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    return None