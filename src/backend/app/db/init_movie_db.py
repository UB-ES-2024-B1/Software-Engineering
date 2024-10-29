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
        
movies_data = [
    {
        "title": "Avatar: The Way of Water",
        "description": "James Cameron returns to the world of Pandora. Set a decade plus after events of the first film, this breathtaking new movie tells the story of the Sully family and introduces audiences to the majestic ocean tulkun.",
        "director": "James Cameron",
        "country": "USA",
        "release_date": date(2022, 12, 16),
        "rating": 4.5,
        "rating_count": 50,
        "likes": 100,
        "genres": ["Action", "Adventure", "Science Fiction"],
        "cast_members": ["Sam Worthington", "Zoe Saldana"]
    },
    {
        "title": "Dune: Part Two",
        "description": "Paul Atreides unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family.",
        "director": "Denis Villeneuve",
        "country": "USA",
        "release_date": date(2024, 3, 15),
        "rating": 4.2,
        "rating_count": 45,
        "likes": 90,
        "genres": ["Action", "Adventure", "Science Fiction"],
        "cast_members": ["Timothée Chalamet", "Zendaya"]
    }
]
'''    
movies_data = [{
    "title": "Spider-Man: No Way Home",
    "description": "When Peter Parker's secret identity is discovered, he turns to Doctor Strange to make the world forget that he is Spider-Man.",
    "director": "Jon Watts",
    "country": "USA",
    "release_date": date(2021, 12, 17),
    "rating": 4.7,
    "rating_count": 85000,
    "likes": 200000,
    "genres": ["Action", "Adventure", "Fantasy"],
    "cast_members": ["Tom Holland", "Zendaya"],
    "image": "images/spider-manNoWayHome_cover.jpg"
},
{
    "title": "Barbie",
    "description": "Living in Barbie Land is about being a perfect being in a perfect place. Unless you have a total existential crisis. Or you are a Ken.",
    "director": "Greta Gerwig",
    "country": "USA",
    "release_date": date(2023, 7, 21),
    "rating": 4.3,
    "rating_count": 70000,
    "likes": 180000,
    "genres": ["Comedy", "Adventure", "Fantasy"],
    "cast_members": ["Margot Robbie", "Ryan Gosling"],
    "image": "images/barbie_cover.jpg"
},
{
    "title": "War for the Planet of the Apes",
    "description": "Caesar and his apes face an army of humans in a battle that will determine the fate of both species and the future of the planet.",
    "director": "Matt Reeves",
    "country": "USA",
    "release_date": date(2017, 7, 14),
    "rating": 4.1,
    "rating_count": 40000,
    "likes": 100000,
    "genres": ["Action", "Drama", "Sci-Fi"],
    "cast_members": ["Andy Serkis", "Woody Harrelson"],
    "image": "images/warForThePlanetOfTheApes_cover.jpg"
}
]
'''
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