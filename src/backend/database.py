# backend/database.py

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # Puedes cambiar el nombre del archivo

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
Base = declarative_base()
