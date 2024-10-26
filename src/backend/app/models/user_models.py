# backend/app/models/user_models.py
from sqlmodel import Field, SQLModel
from typing import Union

# Shared properties
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_admin: bool = False
    full_name: Union[str, None] = None  # Optional full name using Union

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)  # Use Union for compatibility
    hashed_password: str

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

class TokenRequest(SQLModel):
    token: str
