# backend/app/api/routes/genre_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db  # Import the get_db function for database session management
from app.crud import genre_crud  # Import CRUD functions for movie operations
from app.models import (Genre)  # Import movie models for input and output
from typing import List

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