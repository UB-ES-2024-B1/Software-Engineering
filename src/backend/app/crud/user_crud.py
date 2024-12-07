# backend/app/crud/user_crud.py
from sqlalchemy.orm import Session
from app.models.user_models import User, UserOut, ListType, MovieList
from app.models.movie_models import Movie
from typing import List

# Function to create a user
def create_user(db: Session, full_name: str, email: str, hashed_password: str, is_admin: bool =False, is_premium: bool = False) -> UserOut:
    db_user = User(full_name=full_name, email=email, hashed_password=hashed_password,is_admin=is_admin, is_premium=is_premium)
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

def delete_user_by_email(db: Session, user_email: str) -> bool:
    """
    Delete a user from the database by their ID.
    :param db: The database session
    :param user_id: The ID of the user to be deleted
    :return: True if the user was deleted, False if not found
    """
    user = db.query(User).filter(User.email == user_email).first()
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

def update_password(db: Session, user_id: int, new_password: str):
    """
    Update the password of an existing user in the database by ID.
    :param db: Database session
    :param user_id: The ID of the user to update
    :param new_password: The new password
    :return: Updated User object
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.hashed_password = new_password
        db.commit()
        db.refresh(user)
        return user
    return None


def update_user_by_email(db: Session, email: str, user_data: dict):
    # Find the user by email
    user = db.query(User).filter(User.email == email).first()
    
    # If the user doesn't exist, return None
    if not user:
        return None
    
    # Update the user's fields
    for key, value in user_data.items():
        setattr(user, key, value)
    
    # Commit the transaction
    db.commit()
    db.refresh(user)
    
    return user

# Upgrade user to premium
def upgrade_to_premium_by_email(db: Session, user_email: str) -> User:
    """
    Method to update the model/database to premium user by email
    """
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        return None
    user.is_premium = True
    db.commit()
    db.refresh(user)
    return user

# Downgrade user to premium
def downgrade_to_premium_by_email(db: Session, user_email: str) -> User:
    """
    Method to downgrade the model/database to premium user by email
    """
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        return None
    user.is_premium = False
    db.commit()
    db.refresh(user)
    return user

# Create a new list for a user by email
def create_list_by_email(db: Session, user_email: str, list_name: str) -> ListType:
    """
    Method to create a new list for a premium user by email.
    """
    # Fetch the user by email
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        return None
    if not user.is_premium:
        return None

    # Check if a list with the same name already exists for this user
    existing_list = db.query(ListType).filter(
        ListType.created_by_user_email == user_email,
        ListType.name == list_name,
    ).first()
    if existing_list:
        return None

    # Create a new list
    new_list = ListType(name=list_name, created_by_user_email=user_email, user_id=user.id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

# Method for get the entire list of given name of a user
def get_list_type_by_name(session: Session, name: str, user_email: str) -> ListType:
    """Retrieve a list type by its name."""
    # Check if the user exists first
    user = session.query(User).filter(User.email == user_email).first()
    if not user:
        # If the user does not exist, return None
        return None

    # Now check if the ListType exists for the given name and the user's email
    list_type = session.query(ListType).filter(
        ListType.name == name,
        ListType.created_by_user_email == user_email
    ).first()
    if not list_type:
       return None
    
    return list_type

# Method for get all list of a user with email
def get_user_lists_by_email(db: Session, user_email: str)  -> List[ListType]:
    """
    Fetch all lists created by a user, identified by their email.
    :param db: Database session
    :param user_email: The email of the user whose lists we want to fetch
    :return: List of ListType objects if the user has lists, otherwise an empty list
    """
    # Fetch user by email
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        return None  # Return None if user is not found
    
    # Fetch the lists associated with this user
    lists = db.query(ListType).filter(ListType.created_by_user_email == user_email).all()
    return lists

# Add a movie to list name by movie id
def add_movie_to_list(db: Session, user_email: str, list_name: str, movie_id: int) -> MovieList:
    """
    Add a movie to the user's list.
    :param db: Database session
    :param user_email: The email of the user who owns the list
    :param list_name: The name of the list
    :param movie_id: The ID of the movie to be added
    """
    # Retrieve the list
    list_type = db.query(ListType).filter(
        ListType.name == list_name,
        ListType.created_by_user_email == user_email
    ).first()
    # Check if movie exists 
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return None
    # Check if the movie already exists in the list
    existing_movie = db.query(MovieList).filter(
        MovieList.list_type_id == list_type.id,
        MovieList.movie_id == movie_id
    ).first()

    if existing_movie:
        return None
    
    # Add movie to the list
    new_movie_list = MovieList(list_type_id=list_type.id, movie_id=movie_id)
    db.add(new_movie_list)
    db.commit()
    db.refresh(new_movie_list)
    return new_movie_list
