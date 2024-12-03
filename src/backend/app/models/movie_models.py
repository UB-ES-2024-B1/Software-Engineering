from sqlmodel import Field, SQLModel, Relationship
from datetime import date
from typing import Optional, List, Union
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON

from app.models.comments_model import Thread

from app.models.user_models import *


# Association table for the many-to-many relationship
class MovieGenre(SQLModel, table=True):
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id", primary_key=True)
    genre_id: Optional[int] = Field(default=None, foreign_key="genre.id", primary_key=True)

# Model to link Movies and Cast (Relation N-N)
class MovieCast(SQLModel, table=True):
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id", primary_key=True)
    cast_member_id: Optional[int] = Field(default=None, foreign_key="castmember.id", primary_key=True)

class Genre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str = Field(unique=True, index=True)
    movies: List["Movie"] = Relationship(back_populates="genres", link_model=MovieGenre)

# Model for the cast member
class CastMember(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str 
    movies: List["Movie"] = Relationship(back_populates="cast_members", link_model=MovieCast)  # Reference to movies

# Model for input validation (movie creation)
class MovieBase(SQLModel):  
    title: str = Field(unique=True, index=True)
    description: Optional[str] = None
    director: Optional[str] = None
    country: Optional[str] = None
    release_date: Optional[date] = None
    rating: Optional[float] = Field(default=0, ge=0, le=5)  # Rating between 0 and 5
    rating_count: Optional[int] = Field(default=0) 
    likes: Optional[int] = Field(default=0) 
    image: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    trailer: Optional[str] = None

# Model for post a movie
class MovieIn(MovieBase):
    genres: Optional[List[str]]
    cast_members: Optional[List[str]]

# Database model, database table inferred from class name
class Movie(MovieBase, table=True):
    id: Union[int] = Field(default=None, primary_key=True)  # ID as primary key
    # Establishing the many-to-many relationship
    genres: List["Genre"] = Relationship(back_populates="movies", link_model=MovieGenre)
    cast_members: List["CastMember"] = Relationship(back_populates='movies', link_model=MovieCast)
    threads: List[Thread] = Relationship()  # Relationship to comments
    users: List["User"] = Relationship(back_populates="movies", link_model=MovieUser)


# Model for response from the API
class MovieOut(MovieBase):
    id: int
    genres: List[Genre]  # List of genres
    cast_members: List[CastMember]  # List of cast members

# Model for updating a movie
class MovieUpdate(MovieBase):
    id: int

# Just used for update rating
class MovieUpdateRating(SQLModel):
    rating: Optional[float] = Field(default=None, ge=0, le=5)  # Rating between 0 and 5

# Just used for update likes
class MovieUpdateLikes(SQLModel):
    likes: Optional[int] = Field(default=0) 

class Message(SQLModel):
    id: int
