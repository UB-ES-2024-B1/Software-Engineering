# app/api/db/init_movie_db.py
from sqlmodel import Session, select
from app.models import Movie, CastMember, Genre  # Adjust the import based on your project structure
from datetime import date
from app.crud import movie_crud, genre_crud

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
        
# List of movies to be added
'''movies_data = [
    {"title": "Inception", "year": 2010},
    {"title": "The Matrix", "year": 1999},
    {"title": "Interstellar", "year": 2014},
    {"title": "The Godfather", "year": 1972},
    {"title": "Pulp Fiction", "year": 1994},
    {"title": "The Dark Knight", "year": 2008},
    {"title": "Fight Club", "year": 1999},
    {"title": "Forrest Gump", "year": 1994},
    {"title": "The Shawshank Redemption", "year": 1994},
    {"title": "The Lord of the Rings: The Fellowship of the Ring", "year": 2001},
    {"title": "The Social Network", "year": 2010},
    {"title": "The Silence of the Lambs", "year": 1991},
    {"title": "Gladiator", "year": 2000},
    {"title": "The Avengers", "year": 2012},
    {"title": "Titanic", "year": 1997},
    {"title": "The Lion King", "year": 1994},
    {"title": "Goodfellas", "year": 1990},
    {"title": "Braveheart", "year": 1995},
    {"title": "Avatar", "year": 2009},
    {"title": "The Departed", "year": 2006},
]

def init_db(session: Session):
    # Check if the database already has movies to avoid duplicates
    existing_movies = session.exec(select(Movie)).all()
    
    if existing_movies:
        print("Database already contains movies.")
        return

    # Create Movie instances from the movies_data list
    movies = [Movie(**movie) for movie in movies_data]
    
    # Add movies to the session
    session.add_all(movies)
    session.commit()
    print("Sample movies added to the database.")

# Add a new movie with genre and cast associations, checking for existing records first
def add_new_movie(db: Session):
    if len(movie_crud.get_movies(db)) == 0:
        # Step 1: Create a new movie instance with basic details
        new_movie = Movie(
            title="Inception",
            description="A mind-bending thriller about dreams within dreams.",
            director="Christopher Nolan",
            country="USA",
            release_date=date(2010, 7, 16),
            rating=4.8,
            rating_count=10000,
            likes=50000
        )

        # Step 2: Link or create genres
        genres = ["Sci-Fi", "Thriller"]
        for genre_name in genres:
            # Check if the genre already exists
            genre = db.execute(select(Genre).where(Genre.type == genre_name)).scalars().first()
            if not genre:
                # If genre doesn't exist, create it
                genre = Genre(type=genre_name)
                db.add(genre)
                db.commit()  # Commit to get the genre ID
                db.refresh(genre)  # Refresh to ensure the ID is populated
            new_movie.genres.append(genre)  # Link the genre to the movie

        # Step 3: Link or create cast members
        cast_members = ["Leonardo DiCaprio", "Joseph Gordon-Levitt"]
        for member_name in cast_members:
            # Check if the cast member already exists
            cast_member = db.execute(select(CastMember).where(CastMember.name == member_name)).scalars().first()
            if not cast_member:
                # If cast member doesn't exist, create it
                cast_member = CastMember(name=member_name)
                db.add(cast_member)
                db.commit()  # Commit to get the cast member ID
                db.refresh(cast_member)  # Refresh to ensure the ID is populated
            new_movie.cast_members.append(cast_member)  # Link the cast member to the movie

        # Step 4: Add and commit the new movie to the database
        movie_crud.create_movie(db, new_movie)
        print(f"Added new movie: {new_movie.title} with ID {new_movie.id}")'''