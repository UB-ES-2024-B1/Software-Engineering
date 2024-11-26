from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:  # Prevent circular imports during runtime
    from app.models.movie_models import Movie
    from app.models.user_models import User

# Thread model to group comments under a movie
class Thread(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movie.id")  # Foreign key to Movie
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to link threads to their comments
    comments: List["Comment"] = Relationship(back_populates="thread")

# Comment model for user comments within a thread
class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: int = Field(foreign_key="thread.id")  # Foreign key to Thread
    user_id: int = Field(foreign_key="user.id")  # Foreign key to User
    text: str  # Comment text
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    thread: "Thread" = Relationship(back_populates="comments")  # Link to the thread
    user: "User" = Relationship()  # Link to the user
