# backend/app/crud/user_crud.py
from sqlalchemy.orm import Session
from app.models.user_models import User, UserOut,Follow


# Function to create a user
def create_user(db: Session, full_name: str, email: str, hashed_password: str, is_admin: bool =False) -> UserOut:
    db_user = User(full_name=full_name, email=email, hashed_password=hashed_password,is_admin=is_admin)
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

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.full_name == username).first()


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

def get_followers(db: Session, user_id: int) -> list:
    """
    Get followers for a user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return db.query(User).join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == user_id).all()
    return None

def get_followed_users(db: Session, user_id: int) -> list:
    """
    Get followed users for a user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return db.query(User).join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user_id).all()
    return None


# Función para seguir a un usuario
def follow_user(db: Session, follower_id: int, followed_id: int) -> Follow:
    user = db.query(User).filter(User.id == followed_id).first()
    if user:
        # Verificar si ya existe un seguimiento
        existing_follow = db.query(Follow).filter(Follow.follower_id == follower_id, Follow.followed_id == followed_id).first()
        if existing_follow:
            return existing_follow  # Si ya existe, devolverlo en lugar de crear uno nuevo
        else:
            follow = Follow(follower_id=follower_id, followed_id=followed_id)
            db.add(follow)
            db.commit()
            db.refresh(follow)
            return follow
    return None

# Función para dejar de seguir a un usuario
def unfollow_user(db: Session, follower_id: int, followed_id: int) -> bool:
    follow = db.query(Follow).filter(Follow.follower_id == follower_id, Follow.followed_id == followed_id).first()
    if follow:
        db.delete(follow)
        db.commit()
        return True
    return False