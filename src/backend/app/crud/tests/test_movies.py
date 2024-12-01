import unittest
from sqlmodel import Session, create_engine, SQLModel
from app.models import Movie, MovieIn, Genre, CastMember, MovieUser, MovieGenre, MovieCast, MovieUser, Thread
from app.crud.movie_crud import (
    create_movie,
    get_movies,
    get_movie,
    update_movie,
    delete_movie,
    get_movies_sorted_by_release_date,
    get_movies_sorted_by_rating,
    rate_movie,
    like_movie,
    get_movies_sorted_by_likes,
    get_movie_by_title,
    get_movies_sorted_by_related,
    get_movie_by_year,
    is_valid_genre,
    get_movie_by_genre,
    get_movie_by_genre_list,
    remove_movie_like,
    remove_like_movie,
    remove_movie_rating_by_id,
    update_movie_rating_by_id,
    remove_rate_movie,
    get_user_liked_movies,
    get_user_rated_movies
)
from fastapi import HTTPException
import logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# Initialize test database (SQLite in-memory)
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=False)

# Create tables
SQLModel.metadata.create_all(engine)

class TestMovieCrud(unittest.TestCase):
    def setUp(self):
        # Create a new session for each test
        self.db = Session(engine)
        #SQLModel.metadata.create_all(engine)  # Recreate the schema
    
        # Populate initial data
        self.db.add(Genre(type="Action"))
        self.db.add(Genre(type="Drama"))
        self.db.add(CastMember(name="John Doe"))
        self.db.commit()

    def tearDown(self):
        # Clear all records from the database
        self.db.rollback()
        self.db.query(Movie).delete()
        self.db.query(Genre).delete()
        self.db.query(CastMember).delete()
        self.db.query(MovieGenre).delete()
        self.db.query(MovieCast).delete()
        self.db.query(MovieUser).delete()
        self.db.query(Thread).delete()
        self.db.commit()

    def test_create_movie(self):
        # Test movie creation
        movie_data = MovieIn(
            title="Test Movie",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )

        movie = create_movie(self.db, movie_data)
        self.assertEqual(movie.title, "Test Movie")
        self.assertEqual(len(movie.genres), 1)
        self.assertEqual(len(movie.cast_members), 1)

    def test_get_movies(self):
        # Test getting all movies
        movie_data = MovieIn(
            title="Test Movie 2",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        create_movie(self.db, movie_data)

        movies = get_movies(self.db)
        self.assertGreater(len(movies), 0)


    def test_get_movie(self):
        # Test getting a movie by ID
        movie_data = MovieIn(
            title="Test Movie",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)

        fetched_movie = get_movie(self.db, movie.id)
        self.assertEqual(fetched_movie.title, "Test Movie")

    def test_update_movie(self):
        # Test updating a movie
        movie_data = MovieIn(
            title="Test Movie",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)

        updated_data = MovieIn(
            title="Updated Movie",
            description="An updated movie",
            director="New Director",
            country="New Country",
            release_date="2025-01-01",
            rating=5.0,
            rating_count=15,
            likes=10,
            genres=["Drama"],
            cast_members=["John Doe"]
        )
        updated_movie = update_movie(self.db, movie.title, updated_data)
        self.assertEqual(updated_movie.title, "Updated Movie")
        self.assertEqual(updated_movie.director, "New Director")
        self.assertEqual(len(updated_movie.genres), 1)

    def test_delete_movie(self):
        # Test deleting a movie
        movie_data = MovieIn(
            title="Test Movie",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)

        result = delete_movie(self.db, movie.id)
        self.assertTrue(result)

        # Ensure movie is deleted
        fetched_movie = get_movie(self.db, movie.id)
        self.assertIsNone(fetched_movie)

    def test_rate_movie(self):
        # Test rating a movie
        movie_data = MovieIn(
            title="Test Movie",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)

        # Rate movie by user_id=1
        movie_user = rate_movie(self.db, 1, movie.id, 4.0)
        self.assertEqual(movie_user.rating, 4.0)

        fetched_movie = get_movie(self.db, movie.id)      
        self.assertEqual(fetched_movie.rating_count, 11)


    def test_like_movie(self):
        # Test liking a movie
        movie_data = MovieIn(
            title="Test Movie",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)

        # Like movie by user_id=1
        movie_user = like_movie(self.db, 1, movie.id)
        self.assertTrue(movie_user.liked)

    def test_get_movies_sorted_by_release_date(self):
        # Test sorting movies by release date
        movie_data_1 = MovieIn(
            title="Test Movie 1",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )

        movie_data_2 = MovieIn(
            title="Test Movie 2",
            description="Another great movie",
            director="Director",
            country="Country",
            release_date="2025-01-01",
            rating=4.0,
            rating_count=8,
            likes=4,
            genres=["Drama"],
            cast_members=["Jane Doe"]
        )

        create_movie(self.db, movie_data_1)
        create_movie(self.db, movie_data_2)

        movies_sorted = get_movies_sorted_by_release_date(self.db)
        self.assertEqual(movies_sorted[0].title, "Test Movie 1")
        self.assertEqual(movies_sorted[1].title, "Test Movie 2")
        

    def test_get_movie_by_title(self):
        # Test getting a movie by title
        movie_data = MovieIn(
            title="Test Movie",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)

        fetched_movie = get_movie_by_title(self.db, "Test Movie")
        self.assertEqual(fetched_movie.title, "Test Movie")

    def test_get_movies_sorted_by_rating(self):
        # Test sorting movies by rating
        movie_data_1 = MovieIn(
            title="Test Movie 1",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )

        movie_data_2 = MovieIn(
            title="Test Movie 2",
            description="Another great movie",
            director="Director",
            country="Country",
            release_date="2025-01-01",
            rating=4.0,
            rating_count=8,
            likes=4,
            genres=["Drama"],
            cast_members=["Jane Doe"]
        )

        create_movie(self.db, movie_data_1)
        create_movie(self.db, movie_data_2)

        movies_sorted = get_movies_sorted_by_rating(self.db)
        self.assertEqual(movies_sorted[0].title, "Test Movie 1")
        self.assertEqual(movies_sorted[1].title, "Test Movie 2")

    def test_get_movies_sorted_by_likes(self):
        # Test sorting movies by likes
        movie_data_1 = MovieIn(
            title="Test Movie 1",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=10,
            genres=["Action"],
            cast_members=["John Doe"]
        )

        movie_data_2 = MovieIn(
            title="Test Movie 2",
            description="Another great movie",
            director="Director",
            country="Country",
            release_date="2025-01-01",
            rating=4.0,
            rating_count=8,
            likes=5,
            genres=["Drama"],
            cast_members=["Jane Doe"]
        )

        create_movie(self.db, movie_data_1)
        create_movie(self.db, movie_data_2)

        movies_sorted = get_movies_sorted_by_likes(self.db)
        self.assertEqual(movies_sorted[0].title, "Test Movie 1")
        self.assertEqual(movies_sorted[1].title, "Test Movie 2")

    def test_get_movies_sorted_by_related(self):
        # Test sorting movies by related attributes (genre, cast, director)
        movie_data_1 = MovieIn(
            title="Test Movie 1",
            description="A great movie",
            director="Director A",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )

        movie_data_2 = MovieIn(
            title="Test Movie 2",
            description="Another great movie",
            director="Director A",
            country="Country",
            release_date="2025-01-01",
            rating=4.0,
            rating_count=8,
            likes=4,
            genres=["Action"],
            cast_members=["John Doe"]
        )

        movie_data_3 = MovieIn(
            title="Test Movie 3",
            description="A thrilling movie",
            director="Director B",
            country="Country",
            release_date="2026-01-01",
            rating=3.5,
            rating_count=5,
            likes=2,
            genres=["Drama"],
            cast_members=["Jane Doe"]
        )

        create_movie(self.db, movie_data_1)
        create_movie(self.db, movie_data_2)
        create_movie(self.db, movie_data_3)

        related_movies = get_movies_sorted_by_related(self.db, "Test Movie 1")
        self.assertEqual(related_movies[0].title, "Test Movie 2")  # Director matches, so it should be prioritized
        self.assertEqual(related_movies[1].title, "Test Movie 3")  # No match but still related by genre

    def test_get_movie_by_year(self):
        # Test getting movies by release year
        movie_data_1 = MovieIn(
            title="Test Movie 1",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )

        movie_data_2 = MovieIn(
            title="Test Movie 2",
            description="Another great movie",
            director="Director",
            country="Country",
            release_date="2025-01-01",
            rating=4.0,
            rating_count=8,
            likes=4,
            genres=["Drama"],
            cast_members=["Jane Doe"]
        )

        create_movie(self.db, movie_data_1)
        create_movie(self.db, movie_data_2)

        movies_2024 = get_movie_by_year(self.db, 2024)
        self.assertEqual(len(movies_2024), 1)
        self.assertEqual(movies_2024[0].title, "Test Movie 1")

    def test_is_valid_genre(self):
        # Test checking if a genre is valid
        valid_genre = "Action"
        invalid_genre = "Nonexistent Genre"

        self.assertTrue(is_valid_genre(self.db, valid_genre))
        self.assertFalse(is_valid_genre(self.db, invalid_genre))

    def test_get_movie_by_genre(self):
        # Test getting movies by genre
        movie_data_1 = MovieIn(
            title="Test Movie 1",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )

        movie_data_2 = MovieIn(
            title="Test Movie 2",
            description="Another great movie",
            director="Director",
            country="Country",
            release_date="2025-01-01",
            rating=4.0,
            rating_count=8,
            likes=4,
            genres=["Drama"],
            cast_members=["Jane Doe"]
        )

        create_movie(self.db, movie_data_1)
        create_movie(self.db, movie_data_2)

        action_movies = get_movie_by_genre(self.db, "Action")
        self.assertEqual(len(action_movies), 1)
        self.assertEqual(action_movies[0].title, "Test Movie 1")

    def test_get_movie_by_genre_list(self):
        # Test getting movies by a list of genres
        movie_data_1 = MovieIn(
            title="Test Movie 1",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action", "Drama"],
            cast_members=["John Doe"]
        )

        movie_data_2 = MovieIn(
            title="Test Movie 2",
            description="Another great movie",
            director="Director",
            country="Country",
            release_date="2025-01-01",
            rating=4.0,
            rating_count=8,
            likes=4,
            genres=["Action"],
            cast_members=["Jane Doe"]
        )

        create_movie(self.db, movie_data_1)
        create_movie(self.db, movie_data_2)

        movies = get_movie_by_genre_list(self.db, ["Action", "Drama"])
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0].title, "Test Movie 1")

    def test_get_user_rated_movies(self):
        # Test getting movies rated by a user
        movie_data = MovieIn(
            title="Test Movie 1",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)
        
        # Rate movie by user_id=1
        movie_user = rate_movie(self.db, 1, movie.id, 4.0)
        
        rated_movies = get_user_rated_movies(self.db, 1)
        self.assertEqual(len(rated_movies), 1)
        self.assertEqual(rated_movies[0]["title"], "Test Movie 1")

    def test_get_user_liked_movies(self):
        # Test getting movies liked by a user
        movie_data = MovieIn(
            title="Test Movie 2",
            description="Another great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)
        
        # Like movie by user_id=1
        movie_user = like_movie(self.db, 1, movie.id)
        
        liked_movies = get_user_liked_movies(self.db, 1)
        self.assertEqual(len(liked_movies), 1)
        self.assertEqual(liked_movies[0], "Test Movie 2")

    def test_remove_movie_rating_by_id(self):
        # Test removing a rating from a movie by a user
        movie_data = MovieIn(
            title="Test Movie 3",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)
        
        # Rate movie by user_id=1
        movie_user = rate_movie(self.db, 1, movie.id, 4.0)
        
        movie_after_removal = remove_movie_rating_by_id(self.db, movie.id, 1)

        # Check that the movie rating has been updated correctly
        self.assertEqual(movie_after_removal.rating_count, 10)

    def test_update_movie_rating_by_id(self):
        # Test updating a movie's rating by movie ID
        movie_data = MovieIn(
            title="Test Movie",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )

        movie = create_movie(self.db, movie_data)
        
        # Check the movie rating before update
        self.assertEqual(movie.rating, 4.5)
        self.assertEqual(movie.rating_count, 10)
        
        # Update the movie rating
        new_rating = 5.0
        updated_movie = update_movie_rating_by_id(self.db, movie.id, new_rating)
        
        # Check that the movie rating has been updated correctly
        self.assertEqual(updated_movie.rating_count, 11)
        


    def test_remove_rate_movie(self):
        # Test removing a rate from a movie by a user
        movie_data = MovieIn(
            title="Test Movie 4",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)
        
        # Rate movie by user_id=1
        movie_user = rate_movie(self.db, 1, movie.id, 4.0)

        movie_user_after_removal = remove_rate_movie(self.db, 1, movie.id)
        self.assertIsNone(movie_user_after_removal.rating)

    def test_remove_movie_like(self):
        # Test removing a like from a movie by a user
        movie_data = MovieIn(
            title="Test Movie 5",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)
        
        # Like movie by user_id=1
        movie_user = like_movie(self.db, 1, movie.id)

        movie_after_removal = remove_movie_like(self.db, movie.id, 1)
        self.assertEqual(movie_after_removal.likes, 5)

    def test_remove_like_movie(self):
        # Test removing a like from a movie by a user
        movie_data = MovieIn(
            title="Test Movie 6",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)
        
        # Like movie by user_id=1
        movie_user = like_movie(self.db, 1, movie.id)

        movie_user_after_removal = remove_like_movie(self.db, 1, movie.id)
        self.assertFalse(movie_user_after_removal.liked)
