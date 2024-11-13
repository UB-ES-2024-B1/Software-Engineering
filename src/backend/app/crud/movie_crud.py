# backend/app/crud/movie_crud.py
from sqlmodel import Session, select
from app.models import (Movie, MovieIn, MovieOut, MovieUpdate, MovieUpdateRating, MovieUpdateLikes, Genre, CastMember, MovieGenre, MovieCast) 
from typing import List
from fastapi import File, UploadFile
from sqlalchemy import extract

# Function to create a new movie
def create_movie(db: Session, movie: MovieIn, file: UploadFile = File(None)) -> MovieOut:
    # Check if a movie with the same title already exists
    # Create new movie instance
    db_movie = Movie(
        title=movie.title,
        description=movie.description,
        director=movie.director,
        country=movie.country,
        release_date=movie.release_date,
        rating=movie.rating,
        rating_count=movie.rating_count,
        likes=movie.likes,
        image=movie.image
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

    return MovieOut.from_orm(db_movie)  # Use model_validate instead of from_orm

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
'''
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
'''

# Function to update a movie by title
def update_movie(db: Session, movie_title: str, movie_data: MovieUpdate) -> MovieOut:
    statement = select(Movie).where(Movie.title == movie_title)
    movie = db.execute(statement).scalars().first()
    if movie:
        for key, value in movie_data.dict(exclude_unset=True).items():
            if key not in ["genres", "cast_members"]:
                setattr(movie, key, value)
        # Handle genres
        movie.genres.clear()
        for genre_name in movie_data.genres or []:  # Use the genres from the input
            genre = db.execute(select(Genre).where(Genre.type == genre_name)).scalars().first()
            if genre is None:
                genre = Genre(type=genre_name)  # Ensure genre type is not None
                db.add(genre)  # Add new genre to the session
            movie.genres.append(genre)  # Associate genre with the movie

        # Handle cast members
        movie.cast_members.clear()
        for cast_name in movie_data.cast_members or []:
            cast_member = db.execute(select(CastMember).where(CastMember.name == cast_name)).scalars().first()
            if cast_member is None:
                cast_member = CastMember(name=cast_name)  # Ensure cast name is not None
                db.add(cast_member)  # Add new cast member to the session
            movie.cast_members.append(cast_member)  # Associate cast member with the movie
        db.add(movie)
        db.commit()
        db.refresh(movie)  # Refresh to get updated data
        return MovieOut.from_orm(movie)  # Use model_validate
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
    result = db.execute(statement).first()
    movie = result[0] if result else None
    if movie:
        db.delete(movie)
        db.commit()
        return True  # Deletion successful
    return False  # Movie not found

# Function to delete a movie by title
def delete_movie_by_title(db: Session, movie_title: str) -> bool:
    statement = select(Movie).where(Movie.title == movie_title)
    result = db.execute(statement).first()
    movie = result[0] if result else None
    if movie:
        db.delete(movie)
        db.commit()
        return True  # Deletion successful
    return False  # Movie not found


# Function get movie by data release
def get_movie_by_year(db: Session, movie_year: int)-> List[MovieOut]:
    statement = select(Movie).where(extract('year', Movie.release_date) == movie_year)
    return db.execute(statement).scalars().all()