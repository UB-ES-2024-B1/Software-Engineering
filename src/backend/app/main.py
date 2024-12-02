import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api.routes import user_routes, movie_routes, genre_routes, login_routes, comments_routes
from .db import init_movie_db
from .api.db_utils import get_db
from .db.database import engine, Base
from fastapi import Depends
from sqlalchemy.orm import Session
from .db.database import SessionLocal

# Check for the environment variable USE_SELE_CONFIG to decide on CORS settings
USE_SELE_CONFIG = os.getenv("USE_SELE_CONFIG", "false").lower() == "true"

@asynccontextmanager
async def lifespan(app: FastAPI):
    user_routes.init_db()
    with next(get_db()) as db:
        init_movie_db.add_initial_genres(db)
        init_movie_db.init_db_movies(db)
    yield
    print("Shutting down")
    app.state.db.close()

app = FastAPI(lifespan=lifespan)

# Set dynamic CORS configuration based on the environment
if USE_SELE_CONFIG:
    allow_origins = ["https://filmhub-frontend.azurewebsites.net"]
else:
    allow_origins = ["*"]  # For tests with Selenium

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # Use the dynamic value for allow_origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def read_root():
    return {"message": "Hello, FilmHub!"}

# Import the routes from the other files
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(movie_routes.router, prefix="/movies", tags=["movies"])
app.include_router(genre_routes.router, prefix="/genres", tags=["genres"])
app.include_router(login_routes.router, prefix="/login", tags=["login"])
app.include_router(comments_routes.router, prefix="/comments", tags=["comments"])
