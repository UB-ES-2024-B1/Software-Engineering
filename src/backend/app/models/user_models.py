# backend/app/models/user_models.py
from app.models.comments_model import Comment
from sqlmodel import Field, SQLModel, Relationship, Enum
from typing import Union, Optional, List

class ProfileVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    ONLY_FOLLOWERS = "only_followers"

# Shared properties
class UserBase(SQLModel):
    class Config:
        arbitrary_types_allowed = True  # Allow enums or arbitrary types

    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_admin: bool = False
    full_name: Union[str, None] = None  # Optional full name using Union
    img_url: Union[str, None] = None  # Optional SRT link
    img_public_id: Union[str, None] = None  # Optional public ID
    isPublic: str = ProfileVisibility.PUBLIC  # Profile visibility using enum

# The link between movie and movie for rating
class MovieUser(SQLModel, table=True):
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    rating: Optional[float] = Field(default=None, ge=0, le=5)  # User rating between 0 and 5
    liked: Optional[bool] = Field(default=False)  # Whether the user liked the movie
    wished: Optional[bool] = Field(default=False)  # Whether the user liked the movie
 
 # The link between User instances for following using email
class Follow(SQLModel, table=True):
    follower_id: int = Field(foreign_key="user.id", primary_key=True)
    followed_id: int = Field(foreign_key="user.id", primary_key=True)
    
# Database model, database table inferred from class name
class User(UserBase, table=True):
    
    id: Union[int, None] = Field(default=None, primary_key=True)  # Use Union for compatibility
    hashed_password: str
    comments: List["Comment"] = Relationship(back_populates="user")
    # Establish relationship with movies
    movies: List["Movie"] = Relationship(back_populates="users", link_model=MovieUser)


    followers: List["User"] = Relationship(
        sa_relationship_kwargs={
            "secondary": Follow.__table__,
            "primaryjoin": "Follow.followed_id == User.id",
            "secondaryjoin": "Follow.follower_id == User.id",
            "foreign_keys": "[Follow.followed_id, Follow.follower_id]",
            "back_populates": "following",  # Reverse relationship
            "lazy": "select",  # Configura cómo cargar la relación (eager, select, etc.)
        }
    )

    following: List["User"] = Relationship(
        sa_relationship_kwargs={
            "secondary": Follow.__table__,
            "primaryjoin": "Follow.follower_id == User.id",
            "secondaryjoin": "Follow.followed_id == User.id",
            "foreign_keys": "[Follow.follower_id, Follow.followed_id]",
            "back_populates": "followers",  # Reverse relationship
            "lazy": "select",
        }
    )



# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int

class UserUpdate(SQLModel):
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    is_active: Union[bool, None] = None
    is_admin: Union[bool, None] = None
    img_url: Union[str, None] = None  # Optional update for SRT link
    img_public_id: Union[str, None] = None  # Optional update for public ID
    public: Union[bool, None] = None  # Optional update for public profile
    
class TokenRequest(SQLModel):
    token: str

class FollowOut(Follow):
    class Config:
         from_attributes = True  # Actualización a Pydantic v2




