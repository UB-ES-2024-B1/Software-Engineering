from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .db.database import engine, Base
from fastapi import Depends
from sqlalchemy.orm import Session
from .db.database import SessionLocal
from contextlib import asynccontextmanager
from .api.routes import user_routes, movie_routes, genre_routes, login_routes
from .db import init_movie_db
from .api.dependencies import get_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    user_routes.init_db()
    print("Database initialized")
    yield
    print("Shutting down")
    app.state.db.close()

app = FastAPI(lifespan=lifespan)



# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Permitir peticiones desde este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todas las cabeceras
)

@app.get("/")
async def read_root():
    return {"message": "Hello, FilmHub!"}

# Import the routes from the other files
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(movie_routes.router, prefix="/movies", tags=["movies"])
app.include_router(genre_routes.router, prefix="/genres", tags=["genres"])
app.include_router(login_routes.router, prefix="/login",tags=["login"])


# Doing this before starting the app
@app.on_event("startup")
def startup_event():
    user_routes.init_db()
    with next(get_db()) as db:
        #init_movie_db.add_new_movie(db)  # Pass the session instance to the function
        init_movie_db.add_initial_genres(db)
        init_movie_db.init_db_movies(db)
    #init_movie_db(Session)  # Initialize the database with sample movies
    print("Database initialized")
