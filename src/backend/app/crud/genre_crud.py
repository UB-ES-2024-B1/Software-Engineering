# backend/app/crud/genre_crud.py
from sqlmodel import Session, select
from app.models.movie_models import Genre
from typing import List

# Function to get a list of movies with pagination
def get_genres(db: Session, skip: int = 0, limit: int = 100) -> List[Genre]:
    statement = select(Genre).offset(skip).limit(limit)
    results = db.execute(statement).scalars().all()
    return [Genre.model_validate(movie) for movie in results]  # Use model_validate