import unittest
import pytest
from datetime import datetime, timezone, timedelta
from fastapi.exceptions import HTTPException
from sqlmodel import Session, create_engine, SQLModel
from app.models import Movie, MovieIn, Genre, CastMember, MovieGenre, MovieCast, MovieUser, Thread, Comment, User
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
    get_user_rated_movies,
    add_movie_wish,
    wish_movie,
    get_user_wished_movies,
    remove_movie_wish,
    remove_wish_movie,
    delete_movie_by_title,
    get_movies_by_input,
    add_movie_like,
    get_all_ratings,
    format_time_difference

)

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
        self.db.query(Comment).delete()
        self.db.query(User).delete()
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
            genres=["Action", "Fantasy"],
            cast_members=["John Doe"]
        )

        movie = create_movie(self.db, movie_data)
        self.assertEqual(movie.title, "Test Movie")
        self.assertEqual(len(movie.genres), 2)
        self.assertEqual(len(movie.cast_members), 1)

    def test_create_existing_movie(self):
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
        create_movie(self.db, movie_data)

        with pytest.raises(HTTPException) as exc_info:
            create_movie(self.db, movie_data)

        # Check the exception details
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "A movie with this title already exists."

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
            genres=["Drama", "Mistery"],
            cast_members=["John Doe","Mickey Mouse"]
        )
        updated_movie = update_movie(self.db, movie.title, updated_data)
        self.assertEqual(updated_movie.title, "Updated Movie")
        self.assertEqual(updated_movie.director, "New Director")
        self.assertEqual(len(updated_movie.genres), 2)

    def test_update_non_movie(self):

        updated_data = MovieIn(
            title="Updated Movie",
            description="An updated movie",
            director="New Director",
            country="New Country",
            release_date="2025-01-01",
            rating=5.0,
            rating_count=15,
            likes=10,
            genres=["Drama", "Mistery"],
            cast_members=["John Doe","Mickey Mouse"]
        )
        updated_movie = update_movie(self.db, "Test movie", updated_data)
        self.assertIsNone(updated_movie)

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

    def test_delete_non_movie(self):

        result = delete_movie(self.db, 1)
        self.assertFalse(result)

    def test_delete_movie_by_title(self):
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

        result = delete_movie_by_title(self.db, movie.title)
        self.assertTrue(result)

        # Ensure movie is deleted
        fetched_movie = get_movie(self.db, movie.id)
        self.assertIsNone(fetched_movie)

    def test_delete_non_movie_by_title(self):

        result = delete_movie_by_title(self.db, "Test movie")
        self.assertFalse(result)

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

    def test_rate_movie_2_times(self):
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

        movie_user = rate_movie(self.db, 1, movie.id, 3.0)
        self.assertEqual(movie_user.rating, 3.0)

        fetched_movie = get_movie(self.db, movie.id)      
        self.assertEqual(fetched_movie.rating_count, 11)

    def test_invalid_rate_movie(self):
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

        with pytest.raises(HTTPException) as exc_info:
            rate_movie(self.db, 1, movie.id, 6)

        # Check the exception details
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Rating must be between 0 and 5."
    
    
    def test_remove_movie_rating_no_rating2_times(self):
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
        movie_user = rate_movie(self.db, 1, movie.id, 3.0)
        self.assertEqual(movie_user.rating, 3.0)
        rated_movies = get_user_rated_movies(self.db, 1)
        self.assertEqual(len(rated_movies), 1)

        updated_movie = remove_movie_rating_by_id(self.db, movie_id=movie.id, user_id=1)

        rated_movies = get_user_rated_movies(self.db, 1)
        self.assertEqual(len(rated_movies), 0)

        updated_movie = remove_movie_rating_by_id(self.db, movie_id=movie.id, user_id=1)

        rated_movies = get_user_rated_movies(self.db, 1)
        self.assertEqual(len(rated_movies), 0)

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

    def test_add_like_non_movie(self):
        movie_user = add_movie_like(self.db, 1)
        self.assertIsNone(movie_user)

    def test_like_movie_2_times(self):
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

    def test_get_movies_sorted_by_related_of_non_movie(self):

        related_movies = get_movies_sorted_by_related(self.db, "Test Movie 1")
        self.assertEqual(len(related_movies), 0)


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

    def test_remove_unique_movie_rating_by_id(self):
        # Test removing a rating from a movie by a user
        movie_data = MovieIn(
            title="Test Movie 3",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=0,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )
        movie = create_movie(self.db, movie_data)
        
        # Rate movie by user_id=1
        movie_user = rate_movie(self.db, 1, movie.id, 4.0)
        
        movie_after_removal = remove_movie_rating_by_id(self.db, movie.id, 1)

        # Check that the movie rating has been updated correctly
        self.assertEqual(movie_after_removal.rating_count, 0)

    def test_remove_rate_non_existing_movie(self):
        with pytest.raises(HTTPException) as exc_info:
            remove_movie_rating_by_id(self.db, 9999, 1)

        # Check the exception details
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Movie not found"


    def test_remove_rate_movie_not_rated_by_id(self):
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
        
        
        with pytest.raises(HTTPException) as exc_info:
            remove_movie_rating_by_id(self.db, movie.id, 1)

        # Check the exception details
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "No rating to remove"


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
        
    def test_update_non_movie_rating_by_id(self):        
        # Update the movie rating
        new_rating = 5.0
        updated_movie = update_movie_rating_by_id(self.db, 1, new_rating)
        
        self.assertIsNone(updated_movie)

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

    def test_remove_rate_movie_not_rated(self):
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
        
        
        with pytest.raises(HTTPException) as exc_info:
            remove_rate_movie(self.db, 1, movie.id)

        # Check the exception details
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "No rating to remove"



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

    def test_remove_non_exixting_movie_like(self):
        with pytest.raises(HTTPException) as exc_info:
            remove_movie_like(self.db, 999999, 1)

        # Check the exception details
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Movie not found"

    def test_remove_movie_non_liked_intern(self):
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
        
        with pytest.raises(HTTPException) as exc_info:
            remove_movie_like(self.db, movie.id, 1)

        # Check the exception details
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "User hasn't liked the movie"

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

    def test_remove_movie_non_liked(self):
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
        
        with pytest.raises(HTTPException) as exc_info:
            remove_like_movie(self.db, 1, movie.id)

        # Check the exception details
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "No like to remove"

    def test_wish_movie(self):
        # Test adding a new wish for a movie by a user
        movie_data = MovieIn(
            title="Test Movie 1",
            description="A must-watch movie",
            director="Famous Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=0,
            genres=["Drama"],
            cast_members=["Actor A"]
        )
        movie = create_movie(self.db, movie_data)

        # Add a wish for the movie
        movie_user = wish_movie(self.db, user_id=1, movie_id=movie.id)

        # Assert the wish was added
        assert movie_user.wished is True
        assert movie_user.user_id == 1
        assert movie_user.movie_id == movie.id

    def test_wish_movie_2_times(self):
        # Test adding a new wish for a movie by a user
        movie_data = MovieIn(
            title="Test Movie 1",
            description="A must-watch movie",
            director="Famous Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=0,
            genres=["Drama"],
            cast_members=["Actor A"]
        )
        movie = create_movie(self.db, movie_data)

        # Add a wish for the movie
        movie_user = wish_movie(self.db, user_id=1, movie_id=movie.id)

        # Assert the wish was added
        assert movie_user.wished is True
        assert movie_user.user_id == 1
        assert movie_user.movie_id == movie.id

        # Add a wish for the movie again
        movie_user = wish_movie(self.db, user_id=1, movie_id=movie.id)

        # Assert the wish didn't change
        assert movie_user.wished is True
        assert movie_user.user_id == 1
        assert movie_user.movie_id == movie.id

    def test_add_wish_non_movie(self):
        movie_user = add_movie_wish(self.db, 1)
        self.assertIsNone(movie_user)

    def test_get_movies_wished_user(self):
        # Test removing a wish from a movie by a user
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

        # User adds a wish to the movie
        movie_user = wish_movie(self.db, 1, movie.id)
        movies = get_user_wished_movies(self.db, 1)
        
        self.assertEqual(len(movies), 1)
    
    def test_remove_movie_wish(self):
        # Test removing a wish from a movie by a user
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

        # User adds a wish to the movie
        movie_user = wish_movie(self.db, 1, movie.id)
        movies = get_user_wished_movies(self.db, 1)
        
        self.assertEqual(len(movies), 1)
        # Remove the wish
        movie_after_removal = remove_movie_wish(self.db, movie.id, 1)

        movies = get_user_wished_movies(self.db, 1)
        
        self.assertEqual(len(movies), 0)
    

    def test_remove_non_existing_movie_wish(self):
        # Test removing a wish from a non-existent movie
        with pytest.raises(HTTPException) as exc_info:
            remove_movie_wish(self.db, 999999, 1)

        # Check the exception details
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Movie not found"

    def test_remove_movie_wish_not_wished(self):
        # Test removing a wish from a movie that hasn't been wished by the user
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
        movie = create_movie(self.db, movie_data)

        with pytest.raises(HTTPException) as exc_info:
            remove_movie_wish(self.db, movie.id, 1)

        # Check the exception details
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "User hasn't wish the movie"

    def test_remove_wish_movie(self):
        # Test toggling the wish status off
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

        # Add a wish
        movie_user = wish_movie(self.db, 1, movie.id)

        # Remove the wish using remove_wish_movie
        movie_user_after_removal = remove_wish_movie(self.db, 1, movie.id)
        self.assertFalse(movie_user_after_removal.wished)

    def test_remove_wish_movie_not_wished(self):
        # Test removing a wish that doesn't exist
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

        with pytest.raises(HTTPException) as exc_info:
            remove_wish_movie(self.db, 1, movie.id)

        # Check the exception details
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "No wish to remove"

    def test_get_movies_by_input(self):
        # Create sample movie data
        movie_data_1 = MovieIn(
            title="The Great Adventure",
            description="An epic adventure",
            director="Director 1",
            country="USA",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=["Action"],
            cast_members=["John Doe"]
        )

        movie_data_2 = MovieIn(
            title="Another Adventure",
            description="Another epic tale",
            director="Director 2",
            country="Canada",
            release_date="2023-01-01",
            rating=4.0,
            rating_count=8,
            likes=4,
            genres=["Drama"],
            cast_members=["Jane Doe"]
        )

        movie_data_3 = MovieIn(
            title="Mystery Night",
            description="A mysterious journey",
            director="Director 3",
            country="UK",
            release_date="2022-01-01",
            rating=3.5,
            rating_count=5,
            likes=2,
            genres=["Mystery"],
            cast_members=["Sam Smith"]
        )

        # Add movies to the database
        create_movie(self.db, movie_data_1)
        create_movie(self.db, movie_data_2)
        create_movie(self.db, movie_data_3)

        # Test input search for movies containing "Adventure"
        movies = get_movies_by_input(self.db, "Adventure")
        self.assertEqual(len(movies), 2)
        self.assertTrue(any(movie.title == "The Great Adventure" for movie in movies))
        self.assertTrue(any(movie.title == "Another Adventure" for movie in movies))

        # Test input search for movies containing "Mystery"
        movies = get_movies_by_input(self.db, "Mystery")
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0].title, "Mystery Night")

        # Test input search with case insensitivity
        movies = get_movies_by_input(self.db, "adventure")
        self.assertEqual(len(movies), 2)
        self.assertTrue(any(movie.title == "The Great Adventure" for movie in movies))
        self.assertTrue(any(movie.title == "Another Adventure" for movie in movies))

        # Test input search with no matching movies
        movies = get_movies_by_input(self.db, "Sci-Fi")
        self.assertEqual(len(movies), 0)
    
    def test_seconds_ago(self):
        self.assertEqual(format_time_difference(10), "10 seconds ago")

    def test_minutes_ago(self):
        self.assertEqual(format_time_difference(120), "2 minutes ago")

    def test_hours_ago(self):
        self.assertEqual(format_time_difference(7200), "2 hours ago")

    def test_days_ago(self):
        self.assertEqual(format_time_difference(172800), "2 days ago")

    def test_weeks_ago(self):
        self.assertEqual(format_time_difference(1209600), "2 weeks ago")

    def test_months_ago(self):
        self.assertEqual(format_time_difference(5184000), "2 months ago")

    def test_years_ago(self):
        self.assertEqual(format_time_difference(63072000), "2 years ago")

    def test_empty_results(self):
        results = get_all_ratings(self.db, skip=0, limit=10)
        self.assertEqual(len(results), 0)

    def test_get_all_ratings(self):
        # Create the movie object
        movie = Movie(id=1, title="Test Movie", image=["test_image_url"])
        user = User(id=1, 
                full_name="Test User", 
                img_url="user_image_url", 
                isPublic=True, 
                email="testuser@example.com", 
                hashed_password="hashed_password_for_testing")  # Use a dummy hashed password

        # Create the movie-user relation object with a rating
        movie_user = MovieUser(movie_id=1, user_id=1, rating=5.0)

        # Create a comment object
        comment = Comment(
            thread_id=1,
            user_id=1,
            text="Great movie!",
            created_at=datetime.now(timezone.utc) - timedelta(days=2)
        )

        # Add objects to the session
        self.db.add(movie)
        self.db.add(user)
        self.db.add(movie_user)
        self.db.add(comment)

        # Commit the transaction
        self.db.commit()

        # Call the function to get ratings
        results = get_all_ratings(self.db, skip=0, limit=10)
        
        # Validate results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["movie_id"], movie.id)
        self.assertEqual(results[0]["title"], movie.title)
        self.assertEqual(results[0]["rating"], movie_user.rating)
        self.assertEqual(results[0]["full_name"], "Test User")
        self.assertEqual(results[0]["first_comment"], "Great movie!")
        self.assertIn("2 days ago", results[0]["time_since_comment"])
