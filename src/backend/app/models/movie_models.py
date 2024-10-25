# backend/app/models/movie_models.py
from sqlmodel import Field, SQLModel
from datetime import date
from typing import Optional, List, Union

# Model for input validation (movie creation)
class MovieBase(SQLModel):
    name: str = Field(default=None, primary_key=True)
    description: Optional[str] = None
    genre: List[str] = Field(default_factory=list)
    director: Optional[str] = None
    cast: Optional[List[str]] = Field(default_factory=list)
    country: Optional[str] = None
    release_date: Optional[date] = None
    rating: Optional[float] = Field(default=None, ge=0, le=5)  # In our case it is from 0 to 5 stars
    rating_count: Optional[int] = Field(default=0) 
    likes: Optional[int] = Field(default=0) 

# Database model, database table inferred from class name
class Movie(MovieBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)  # Use Union for compatibility

# Model for response from the API
class MovieOut(MovieBase):
    id: int

# Model for updating a movie
class MovieUpdate(MovieBase):
    id: int

# Just used for update rating
class MovieUpdateRating(SQLModel):
    rating: Optional[float] = Field(default=None, ge=0, le=5)  # In our case it is from 0 to 5 stars
    rating_count: Optional[int] = Field(default=0) 

# Just used for update likes
class MovieUpdateLikes(SQLModel):
    likes: Optional[int] = Field(default=0) 

class Message(SQLModel):
    id: int