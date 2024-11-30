from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel

if TYPE_CHECKING:  # Prevent circular imports during runtime
    from app.models.movie_models import Movie
    from app.models.user_models import User

class ReportStatus(str, Enum):  # Using str for string representation in the database
    CLEAN = "CLEAN"
    REPORTED = "REPORTED"
    BANNED = "BANNED"

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
    thread_id: int = Field(foreign_key="thread.id")
    user_id: int = Field(foreign_key="user.id")
    user_name: str
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reported: ReportStatus = Field(default=ReportStatus.CLEAN)

    # Relationships
    thread: "Thread" = Relationship(back_populates="comments")
    user: "User" = Relationship()
    reported_by: List["CommentReportedBy"] = Relationship(back_populates="comment")  # Reverse relationship

    
class CommentUpdateRequest(BaseModel):
    text: Optional[str] = None  # Optional text

class CommentReportRequest(BaseModel):
    reported: ReportStatus = ReportStatus.CLEAN  # Optional reported status


class CommentReportedBy(SQLModel, table=True):
    """
    Intermediary table to track which user last changed the report status of a comment.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    comment_id: int = Field(foreign_key="comment.id")  # Foreign key to Comment
    user_id: int = Field(foreign_key="user.id")  # Foreign key to User
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Timestamp of the change

    # Relationships
    comment: "Comment" = Relationship(back_populates="reported_by")  # Removed overlaps
    user: "User" = Relationship()

