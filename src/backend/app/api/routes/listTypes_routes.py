from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.database import SessionLocal  # Import the SessionLocal from database.py
from app.crud import user_crud  # Assuming you have CRUD operations for ListType
from app.api.dependencies import *  # Import the get_db function
from app.models import ListType, MovieList
from typing import List, Optional

router = APIRouter()

# Create a new ListType
@router.post("/{user_email}/{list_name}", response_model=ListType, status_code=status.HTTP_201_CREATED)
def create_list(list_name: str, user_email: str, db: Session = Depends(get_db)):
    """
    Create a new list for a premium user by email.
    :param list_name: The name of the list to be created
    :param user_email: The email of the user who owns the list
    :param db: Database session (injected via dependency)
    :return: The created list type object
    """
    # Create the list if it doesn't already exist
    new_list = user_crud.create_list_by_email(db, user_email, list_name)
    if new_list is None:
        # If new_list is None, raise an HTTPException with a proper message
        raise HTTPException(status_code=400, detail="User not found or unable to create list")
    
    return new_list

# Get a list type by user's email
@router.get("/email/{email}", response_model=List[ListType])
def get_list_type_by_email(user_email: str, db: Session = Depends(get_db)):
    """
    Get a list type by its name and the user's email.
    :param name: The name of the list type
    :param user_email: The email of the user who created the list type
    :param db: Database session (injected via dependency)
    :return: ListType object or 404 if not found
    """
    list_type = user_crud.get_user_lists_by_email(db, user_email=user_email)
    if not list_type:
        raise HTTPException(status_code=404, detail="List type not found")
    return list_type

# Get a list by its name and user's email
@router.get("/list_by_name/{user_email}/{list_name}", response_model=ListType)
def get_list_by_name_and_email(user_email: str, list_name: str, db: Session = Depends(get_db)):
    """
    Get a list by its name and the user's email.
    :param user_email: The email of the user who owns the list
    :param list_name: The name of the list to fetch
    :param db: Database session (injected via dependency)
    :return: The list object or 404 if not found
    """
    list_type = user_crud.get_list_type_by_name(db, user_email=user_email, name=list_name)
    if not list_type:
        raise HTTPException(status_code=404, detail="List not found")
    return list_type

# Add a movie to a user's list
@router.post("/add-movie/{user_email}/{list_name}/{movie_id}", response_model=MovieList)
def add_movie_to_list(user_email: str, list_name: str, movie_id: int, db: Session = Depends(get_db)):
    """
    Add a movie to a list for a given user and list name.
    :param user_email: The email of the user who owns the list
    :param list_name: The name of the list to add the movie to
    :param movie_id: The ID of the movie to add to the list
    :param db: Database session (injected via dependency)
    :return: The updated list object
    """
    lista = user_crud.get_list_type_by_name(db, user_email=user_email, name=list_name)
    if not lista:
        raise HTTPException(status_code=404, detail="List not found")
    list_type = user_crud.add_movie_to_list(db, user_email, list_name, movie_id)
    if not list_type:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return list_type

# Get the list of movie names by list name and user email
@router.get("/movies/{user_email}/{list_name}", response_model=List[str])
def get_movie_names_by_list_name(user_email: str, list_name: str, db: Session = Depends(get_db)):
    """
    Get a list of movie names given the list name and user's email.
    :param user_email: The email of the user who owns the list
    :param list_name: The name of the list to fetch movies for
    :param db: Database session (injected via dependency)
    :return: A list of movie names associated with the list
    """
    # Fetch the list by name and user email
    list_type = user_crud.get_list_type_by_name(db, user_email=user_email, name=list_name)
    if not list_type:
        raise HTTPException(status_code=404, detail="List not found")
  
    # Get the list of movies associated with this list, only return movie names
    movie_names = [movie.movie.title for movie in list_type.movies]
    
    return movie_names

# Delete a list by name and user's email
@router.delete("/{user_email}/{list_name}", status_code=status.HTTP_200_OK)
def delete_list(user_email: str, list_name: str, db: Session = Depends(get_db)):
    """
    Delete a list for a user by email.
    :param user_email: The email of the user who owns the list
    :param list_name: The name of the list to delete
    :param db: Database session (injected via dependency)
    """
    # Call the CRUD function to remove the list
    list_type = user_crud.get_list_type_by_name(db, user_email=user_email, name=list_name)
    if not list_type:
        raise HTTPException(status_code=404, detail="List not found")
    
    # Use CRUD function to delete the list
    user_crud.delete_list_by_name(db, user_email=user_email, list_name=list_name)

    return {"detail": f"List '{list_name}' deleted successfully."}

# Remove a movie from a list by movie id and list name
@router.delete("/remove-movie/{user_email}/{list_name}/{movie_id}", status_code=status.HTTP_200_OK)
def remove_movie_from_list(user_email: str, list_name: str, movie_id: int, db: Session = Depends(get_db)):
    """
    Remove a movie from a user's list.
    :param user_email: The email of the user who owns the list
    :param list_name: The name of the list from which to remove the movie
    :param movie_id: The ID of the movie to remove from the list
    :param db: Database session (injected via dependency)
    """
    # Call the CRUD function to remove the movie from the list
    movie_list_entry = user_crud.remove_movie_from_list_by_email(db, user_email, list_name, movie_id)
    if not movie_list_entry:
        raise HTTPException(status_code=404, detail="Movie not found in the list")
    
    return {"detail": f"Movie ID {movie_id} removed from list '{list_name}'."}

# Get all lists with movies for a user
@router.get("/get-lists-with-movies/{user_email}", response_model=List[dict])
def get_lists_with_movies(user_email: str, db: Session = Depends(get_db)):
    """
    Retrieve all lists with their movies for a user by email.
    :param user_email: The email of the user
    :param db: Database session (injected via dependency)
    :return: A list of lists, each with its movies
    """
    user_lists = user_crud.get_all_lists_with_movies(db, user_email)
    if not user_lists:
        raise HTTPException(status_code=404, detail="No lists found for the user.")
    
    return user_lists
