# backend/app/crud/movie_crud.py
from sqlmodel import Session, select
from app.models.movie_models import Movie, MovieIn, MovieOut, MovieUpdate, MovieUpdateLikes, MovieUpdateRating
from typing import List

# Function to create a new movie
def create_movie(db: Session, movie_data: MovieIn) -> MovieOut:
    # Check if a movie with the same title already exists
    existing_movie = db.execute(select(Movie).where(Movie.title == movie_data.title)).first()
    if existing_movie:
        return None
    
    db.add(movie_data)
    db.commit()
    db.refresh(movie_data)  # Refresh to get the new ID
    return MovieOut.model_validate(movie_data)  # Use model_validate instead of from_orm

# Function to get a list of movies with pagination
def get_movies(db: Session, skip: int = 0, limit: int = 100) -> List[MovieOut]:
    statement = select(Movie).offset(skip).limit(limit)
    results = db.execute(statement).scalars().all()
    return [MovieOut.model_validate(movie) for movie in results]  # Use model_validate

# Function to get a movie by ID
def get_movie(db: Session, movie_id: int) -> MovieOut:
    statement = select(Movie).where(Movie.id == movie_id)
    movie = db.execute(statement).scalars().first()
    if movie:
        return MovieOut.model_validate(movie)  # Use model_validate
    return None  # If movie not found

# CRUDs to get different types of list of movies
def get_movie_by_title(db: Session, movie_title: str) -> MovieOut:
    statement = select(Movie).where(Movie.title == movie_title)
    return db.execute(statement).scalars().first()

def get_movies_sorted_by_release_date(db: Session) -> List[MovieOut]:
    statement = select(Movie).order_by(Movie.release_date)
    return db.execute(statement).scalars().all()

def get_movies_sorted_by_rating(db: Session) -> List[MovieOut]:
    statement = select(Movie).order_by(Movie.rating.desc())  # Assuming higher rating is better
    return db.execute(statement).scalars().all()

def get_movies_sorted_by_likes(db: Session) -> List[MovieOut]:
    statement = select(Movie).order_by(Movie.likes.desc())  # Assuming more likes is better
    return db.execute(statement).scalars().all()

# Function to update a movie by ID
def update_movie(db: Session, movie_id: int, movie_data: MovieUpdate) -> MovieOut:
    statement = select(Movie).where(Movie.id == movie_id)
    movie = db.execute(statement).scalars().first()
    if movie:
        for key, value in movie_data.dict(exclude_unset=True).items():
            setattr(movie, key, value)
        db.add(movie)
        db.commit()
        db.refresh(movie)  # Refresh to get updated data
        return MovieOut.model_validate(movie)  # Use model_validate
    return None  # If movie not found

def update_movie_rating_by_title(db: Session, movie_title: str, new_rating: float):
    # Query the movie by title
    movie = db.query(Movie).filter(Movie.title == movie_title).first()
    
    # If the movie doesn't exist, return None
    if not movie:
        return None
    
    # Calculate the new average rating
    total_rating_sum = movie.rating * movie.rating_count  # Total of all previous ratings
    total_rating_sum += new_rating  # Add the new rating to the total
    movie.rating_count += 1         # Increase the count by 1
    movie.rating = total_rating_sum / movie.rating_count  # Calculate the new average
    
    # Commit the transaction and refresh the instance
    db.commit()
    db.refresh(movie)
    
    return movie

def add_movie_like(db: Session, movie_title: str):
    # Query the movie by title
    movie = db.query(Movie).filter(Movie.title == movie_title).first()
    
    # If the movie doesn't exist, return None
    if not movie:
        return None
    
    # Increment the likes count by 1
    movie.likes += 1
    
    # Commit the transaction and refresh the instance
    db.commit()
    db.refresh(movie)
    
    return movie

# Function to delete a movie by ID
def delete_movie(db: Session, movie_id: int) -> bool:
    statement = select(Movie).where(Movie.id == movie_id)
    movie = db.exec(statement).first()
    if movie:
        db.delete(movie)
        db.commit()
        return True  # Deletion successful
    return False  # Movie not found

# Function to delete a movie by title
def delete_movie_by_title(db: Session, movie_title: str) -> bool:
    statement = select(Movie).where(Movie.title == movie_title)
    movie = db.exec(statement).first()
    if movie:
        db.delete(movie)
        db.commit()
        return True  # Deletion successful
    return False  # Movie not found

