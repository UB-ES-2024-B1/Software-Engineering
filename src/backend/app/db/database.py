# backend/app/db/database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL (In this case, SQLite, but it can be PostgreSQL, MySQL, etc.)
DATABASE_URL = "sqlite:///./filmhub_database.db"  # You can change this to your actual database URL

# Create the SQLAlchemy engine, which manages connections to the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory that allows you to generate sessions to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# MetaData holds all the table definitions and schema information (optional)
metadata = MetaData()

from app.models.user_models import User  # Ensure this import happens
# Base class for all the models (tables). All models should inherit from this base
Base = declarative_base()
