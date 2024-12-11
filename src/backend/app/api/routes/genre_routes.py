# backend/app/api/routes/genre_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.db_utils import get_db  # Import the get_db function for database session management
from app.crud import genre_crud  # Import CRUD functions for movie operations
from app.models import (Genre)  # Import movie models for input and output
from typing import List
from app.scrape_movies import fetch_all_genres

# Create a router for movie-related endpoints
router = APIRouter()

# Endpoint to retrieve a list of genres
@router.get("/", response_model=List[Genre])
def get_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of genres from the database with optional pagination.
    """
    # Call the CRUD function to retrieve movies with pagination
    return genre_crud.get_genres(db, skip=skip, limit=limit)

@router.get("/fromAPI")
def get_genres_from_api():

    genres = fetch_all_genres()
    genre_list = []

    if genres:
        for genre in genres:
            genre_list.append(genre['name'])
        
        return genre_list
    else:
        raise HTTPException(status_code=404, detail="No genres found")
    