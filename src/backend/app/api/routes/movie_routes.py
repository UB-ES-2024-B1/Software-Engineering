# backend/app/api/routes/movie_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import Session, select
from app.api.dependencies import get_db  # Import the get_db function for database session management
from app.crud import movie_crud  # Import CRUD functions for movie operations
from app.models import (Movie, MovieIn, MovieOut, MovieUpdate, MovieUpdateRating, MovieUpdateLikes, Genre, CastMember, MovieGenre, MovieCast)  # Import movie models for input and output
from typing import List

# Create a router for movie-related endpoints
router = APIRouter()

# Endpoint to create a new movie
@router.post("/", response_model=MovieOut)
def create_movie(movie: MovieIn, db: Session = Depends(get_db)):
    """
    Creates a new movie entry in the database.
    
    :param movie: Movie - Pydantic model containing the movie data to create
    :param db: Session - Database session dependency
    :return: MovieOut - Pydantic model representing the created movie's details
    """
    # Call the CRUD function to create a new movie record
    # Check if the email is already registered
    existing_movie = movie_crud.get_movie_by_title(db, movie_title=movie.title)
    if existing_movie:
        raise HTTPException(status_code=400, detail="Movie title already registered")
    
    # Create new movie instance
    db_movie = Movie(
        title=movie.title,
        description=movie.description,
        director=movie.director,
        country=movie.country,
        release_date=movie.release_date,
        rating=movie.rating,
        rating_count=movie.rating_count,
        likes=movie.likes
    )

    # Handle genres
    for genre_name in movie.genres or []:  # Use the genres from the input
        genre = db.execute(select(Genre).where(Genre.type == genre_name)).scalars().first()
        if genre is None:
            genre = Genre(type=genre_name)  # Ensure genre type is not None
            db.add(genre)  # Add new genre to the session
        db_movie.genres.append(genre)  # Associate genre with the movie

    # Handle cast members
    for cast_name in movie.cast_members or []:
        cast_member = db.execute(select(CastMember).where(CastMember.name == cast_name)).scalars().first()
        if cast_member is None:
            cast_member = CastMember(name=cast_name)  # Ensure cast name is not None
            db.add(cast_member)  # Add new cast member to the session
        db_movie.cast_members.append(cast_member)  # Associate cast member with the movie

    # Add movie to the session and commit
    db.add(db_movie)
    db.commit()  # Commit the transaction
    db.refresh(db_movie)  # Refresh to get the updated data

    # Return the created movie details
    return MovieOut.from_orm(db_movie)

# Endpoint to retrieve a list of movies
@router.get("/", response_model=List[MovieOut])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of movies from the database with optional pagination.
    
    :param skip: int - The number of records to skip (default: 0)
    :param limit: int - The maximum number of records to retrieve (default: 100)
    :param db: Session - Database session dependency
    :return: list[MovieOut] - A list of MovieOut models representing each movie
    """
    # Call the CRUD function to retrieve movies with pagination
    return movie_crud.get_movies(db, skip=skip, limit=limit)

# Endpoint to retrieve a single movie by its ID
@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single movie by its ID.
    
    :param movie_id: int - The ID of the movie to retrieve
    :param db: Session - Database session dependency
    :return: MovieOut - The retrieved movie's details
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to get a movie by ID
    movie = movie_crud.get_movie(db=db, movie_id=movie_id)
    # If the movie does not exist, raise a 404 error
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# Endpoint to retrieve a single movie by its title
@router.get("/title/{movie_title}", response_model=MovieOut)
def get_movie_by_title(movie_title: str, db: Session = Depends(get_db)):
    """
    Retrieves a single movie by its title.
    
    :param movie_title: str - The title of the movie to retrieve
    :param db: Session - Database session dependency
    :return: MovieOut - The retrieved movie's details
    :raises HTTPException: 404 if the movie is not found
    """
    movie = movie_crud.get_movie_by_title(db=db, movie_title=movie_title)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# Endpoint to retrieve movies sorted by release date
@router.get("/sorted/release_date", response_model=List[MovieOut])
def get_movies_sorted_by_release_date(db: Session = Depends(get_db)):
    """
    Retrieves a list of movies sorted by release date.
    
    :param db: Session - Database session dependency
    :return: List[MovieOut] - A sorted list of movies by release date
    """
    movies = movie_crud.get_movies_sorted_by_release_date(db=db)
    return movies

# Endpoint to retrieve movies sorted by rating
@router.get("/sorted/rating", response_model=List[MovieOut])
def get_movies_sorted_by_rating(db: Session = Depends(get_db)):
    """
    Retrieves a list of movies sorted by rating.
    
    :param db: Session - Database session dependency
    :return: List[MovieOut] - A sorted list of movies by rating
    """
    movies = movie_crud.get_movies_sorted_by_rating(db=db)
    return movies

# Endpoint to retrieve movies sorted by likes
@router.get("/sorted/likes", response_model=List[MovieOut])
def get_movies_sorted_by_likes(db: Session = Depends(get_db)):
    """
    Retrieves a list of movies sorted by likes.
    
    :param db: Session - Database session dependency
    :return: List[MovieOut] - A sorted list of movies by likes
    """
    movies = movie_crud.get_movies_sorted_by_likes(db=db)
    return movies


# Endpoint to update an existing movie by its ID
@router.put("/{movie_id}", response_model=MovieOut)
def update_movie(movie_id: int, movie_data: MovieIn, db: Session = Depends(get_db)):
    """
    Updates an existing movie's details by its ID.
    
    :param movie_id: int - The ID of the movie to update
    :param movie_data: MovieUpdate - The data to update the movie with
    :param db: Session - Database session dependency
    :return: MovieOut - The updated movie's details
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to update the movie
    updated_movie = movie_crud.update_movie(db, movie_id, movie_data)
    # If the movie does not exist, raise a 404 error
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie

# Endpoint to update only the rating of an existing movie by its title
@router.put("/{movie_title}/rating", response_model=MovieOut)
def update_movie_rating_by_title(movie_title: str, rating_data: MovieUpdateRating, db: Session = Depends(get_db)):
    """
    Updates only the rating of an existing movie by its title.
    
    :param movie_title: str - The title of the movie to update
    :param rating_data: MovieUpdateRating - The new rating data for the movie
    :param db: Session - Database session dependency
    :return: MovieOut - The updated movie's details
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to update the movie's rating by title
    updated_movie = movie_crud.update_movie_rating_by_title(db, movie_title, rating_data.rating)
    
    # If the movie does not exist, raise a 404 error
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return updated_movie

# Endpoint to increment the likes of a movie by its title
@router.put("/{movie_title}/like", response_model=MovieOut)
def add_movie_like(movie_title: str, db: Session = Depends(get_db)):
    """
    Adds one like to the movie's likes count.
    
    :param movie_title: str - The title of the movie to like
    :param db: Session - Database session dependency
    :return: MovieOut - The updated movie details with the incremented like count
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to add a like to the movie
    updated_movie = movie_crud.add_movie_like(db, movie_title)
    
    # If the movie does not exist, raise a 404 error
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return updated_movie

# Endpoint to delete an existing movie by its ID
@router.delete("/id/{movie_id}", response_model=dict)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Deletes a movie from the database by its ID.
    
    :param movie_id: int - The ID of the movie to delete
    :param db: Session - Database session dependency
    :return: dict - A success message if deletion is successful
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to delete the movie
    success = movie_crud.delete_movie(db, movie_id)
    # If the movie does not exist, raise a 404 error
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}

# Endpoint to delete an existing movie by its title
@router.delete("/title/{movie_title}", response_model=dict)
def delete_movie_by_title(movie_title: str, db: Session = Depends(get_db)):
    """
    Deletes a movie from the database by its title.
    
    :param movie_title: str - The title of the movie to delete
    :param db: Session - Database session dependency
    :return: dict - A success message if deletion is successful
    :raises HTTPException: 404 if the movie is not found
    """
    # Call the CRUD function to delete the movie by title
    success = movie_crud.delete_movie_by_title(db, movie_title)
    # If the movie does not exist, raise a 404 error
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}
