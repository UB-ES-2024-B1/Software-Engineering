# app/api/db/init_movie_db.py
from sqlmodel import Session, select
from app.models import Movie, MovieIn, CastMember, Genre  # Adjust the import based on your project structure
from datetime import date, datetime
from app.crud import movie_crud, genre_crud
import json
# Function to add initial genres
def add_initial_genres(db_session):
    if len(genre_crud.get_genres(db_session)) == 0:
        genres = [
            "Action", "Adventure", "Comedy", "Drama", "Fantasy",
            "Historical", "Horror", "Mystery", "Romance",
            "Science Fiction", "Thriller", "Western", "Documentary", 
            "Musical", "Animation"
        ]
        
        for genre_name in genres:
            genre = Genre(type=genre_name)
            db_session.add(genre)
        
        db_session.commit()
        

file_path = 'data_movies.json'

def init_db_movies(db_session):
    if len(movie_crud.get_movies(db_session)) == 0:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Insertar usuarios en la base de datos
        for movie_data in data:
            if 'release_date' in movie_data:
                movie_data['release_date'] = datetime.strptime(movie_data['release_date'], '%Y, %m, %d').date()
            
            movie_crud.create_movie(
                db=db_session,
                movie=MovieIn(**movie_data)
            )
    db_session.close()  # Cerrar la sesión

