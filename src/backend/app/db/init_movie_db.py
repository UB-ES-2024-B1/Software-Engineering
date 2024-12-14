# app/api/db/init_movie_db.py
from sqlmodel import Session, select
from app.models import Movie, MovieIn, CastMember, Genre, Comment, ReportStatus, MovieUser  # Adjust the import based on your project structure
from datetime import date, datetime,timezone
from app.crud import movie_crud, genre_crud, comments_crud
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


file_path_comments = 'data_comments.json'  # Path to the JSON file with data

def init_db_comments(db_session: Session):
    if len(db_session.query(Comment).all()) == 0:  # Only add if there are no existing comments
        with open(file_path_comments, 'r') as file:
            data = json.load(file)

        for movie_data in data:
            movie_id = movie_data['movie_id']

            # Create comments for the existing thread associated with the movie
            for comment_data in movie_data['comments']:
                comment = Comment(
                    thread_id=movie_id,  # Assuming thread_id corresponds to movie_id as a foreign key
                    user_id=comment_data['user_id'],
                    text=comment_data['comment'],
                    created_at= datetime.now(timezone.utc),
                    reported=ReportStatus(comment_data.get('reported', 'CLEAN'))  # Handle potential missing 'reported' field
                )
                db_session.add(comment)

            # Add movie ratings to the MovieUser table
            if 'ratings' in movie_data:
                for rating_data in movie_data['ratings']:
                    movie_user = MovieUser(
                        movie_id=movie_id,
                        user_id=rating_data['user_id'],
                        rating=rating_data.get('rating', None),  # Optional rating value, None if not present
                        liked=rating_data.get('liked', False),  # Optional like flag, default False
                        wished=rating_data.get('wished', False)  # Optional wish flag, default False
                    )
                    db_session.add(movie_user)

        db_session.commit()  # Commit all changes after processing the file