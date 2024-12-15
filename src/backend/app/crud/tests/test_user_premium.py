import unittest
from unittest.mock import MagicMock
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.orm import Session
from app.crud.user_crud import (
    upgrade_to_premium_by_email, downgrade_to_premium_by_email, create_list_by_email,
    get_list_type_by_name, get_user_lists_by_email, add_movie_to_list,
    get_all_lists_with_movies, delete_list_by_name, remove_movie_from_list_by_email,
    delete_movie_links
)
from app.models.user_models import User, UserOut,Follow, ListType, MovieList
from app.models.movie_models import Movie, Genre, CastMember

class TestExtendedUserCRUD(unittest.TestCase):
    def setUp(self):
        """Set up the mock database session."""
        self.db = MagicMock(Session)
        self.user_email = "john@example.com"
        self.fake_user = User(id=1, email=self.user_email, full_name="John Doe", is_premium=False)
        self.fake_premium_user = User(id=2, email="premium@example.com", full_name="Jane Doe", is_premium=True)

    def test_upgrade_to_premium_by_email(self):
        """Test upgrading a user to premium."""
        self.db.query.return_value.filter.return_value.first.return_value = self.fake_user
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.fake_user

        result = upgrade_to_premium_by_email(self.db, user_email=self.user_email)

        self.assertTrue(result.is_premium)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_upgrade_to_premium_by_email_user_not_found(self):
        """Test upgrading a non-existent user to premium."""
        self.db.query.return_value.filter.return_value.first.return_value = None

        result = upgrade_to_premium_by_email(self.db, user_email="nonexistent@example.com")

        self.assertIsNone(result)

    def test_downgrade_to_premium_by_email(self):
        """Test downgrading a premium user."""
        self.db.query.return_value.filter.return_value.first.return_value = self.fake_premium_user
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.fake_premium_user

        result = downgrade_to_premium_by_email(self.db, user_email=self.fake_premium_user.email)

        self.assertFalse(result.is_premium)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    
    def test_create_list_by_email(self):
        """Test creating a new list for a premium user."""
        
        # Mock the User object
        self.fake_premium_user = User(email="premium@example.com", full_name="Jane Doe", is_premium=True, id=2)
        
        # Mock the ListType object
        self.fake_list = ListType(id=1, name="My List", created_by_user_email=self.fake_premium_user.email, user_id=self.fake_premium_user.id)

        # Mock database query
        self.db.query.return_value.filter.return_value.first.side_effect = [self.fake_premium_user, None]

        # Mock commit, add, and refresh methods
        self.db.add.return_value = None
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.fake_list  # Return the created list object when refreshing

        # Call the function to test
        result = create_list_by_email(self.db, user_email=self.fake_premium_user.email, list_name="My List")

        # Assertions to verify the results
        self.assertIsNotNone(result)
        self.db.add.assert_called_once_with(result)  # Ensure that the add method was called once with the result
        self.db.commit.assert_called_once()  # Ensure that commit was called once
        self.db.refresh.assert_called_once_with(result)  # Ensure that refresh was called once with the result

        # Additional checks on the result
        self.assertEqual(result.name, "My List")
        self.assertEqual(result.created_by_user_email, self.fake_premium_user.email)

    def test_create_list_by_email_restricted_name(self):
        """Test creating a list with a restricted name."""
        result = create_list_by_email(self.db, user_email=self.fake_premium_user.email, list_name="Favorite")
        self.assertIsNone(result)

    def test_create_list_by_email_user_not_found(self):
        """Test creating a list for a non-existent user."""
        self.db.query.return_value.filter.return_value.first.return_value = None

        result = create_list_by_email(self.db, user_email="nonexistent@example.com", list_name="My List")

        self.assertIsNone(result)

    def test_get_list_type_by_name(self):
        """Test retrieving a list type by name."""
        fake_list = ListType(id=1, name="My List", created_by_user_email=self.user_email)
        self.db.query.return_value.filter.return_value.first.side_effect = [self.fake_user, fake_list]

        result = get_list_type_by_name(self.db, name="My List", user_email=self.user_email)

        self.assertEqual(result.name, "My List")

    def test_get_list_type_by_name_user_not_found(self):
        """Test retrieving a list for a non-existent user."""
        self.db.query.return_value.filter.return_value.first.return_value = None

        result = get_list_type_by_name(self.db, name="My List", user_email="nonexistent@example.com")

        self.assertIsNone(result)

    def test_add_movie_to_list(self):
        """Test adding a movie to a user's list."""
        # Mock the list, movie, and movie-list entry
        fake_list = ListType(id=1, name="My List", created_by_user_email=self.user_email)
        fake_movie = Movie(id=1, title="Movie Title")
        fake_existing_entry = MovieList(list_type_id=1, movie_id=1)

        # Mock the database query object and its filter().first() behavior
        fake_query_list = MagicMock()
        fake_query_movie = MagicMock()
        fake_query_movie_list = MagicMock()

        # Set up the mock responses for each filter().first()
        fake_query_list.filter.return_value.first.return_value = fake_list  # ListType query
        fake_query_movie.filter.return_value.first.return_value = fake_movie  # Movie query
        fake_query_movie_list.filter.return_value.first.return_value = None  # MovieList query

        # Mock the query method on db to return the appropriate query object
        self.db.query.side_effect = [fake_query_list, fake_query_movie, fake_query_movie_list]

        # Call the function under test
        result = add_movie_to_list(self.db, user_email=self.user_email, list_name="My List", movie_id=1)

        self.assertIsNotNone(result)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()



    def test_add_movie_to_list_duplicate(self):
        """Test adding a duplicate movie to a user's list."""

        # Mock the list, movie, and movie-list entry
        fake_list = ListType(id=1, name="My List", created_by_user_email=self.user_email)
        fake_movie = Movie(id=1, title="Movie Title")
        fake_existing_entry = MovieList(list_type_id=1, movie_id=1)

        # Mock the database query object and its filter().first() behavior
        fake_query_list = MagicMock()
        fake_query_movie = MagicMock()
        fake_query_movie_list = MagicMock()

        # Set up the mock responses for each filter().first()
        fake_query_list.filter.return_value.first.return_value = fake_list  # ListType query
        fake_query_movie.filter.return_value.first.return_value = fake_movie  # Movie query
        fake_query_movie_list.filter.return_value.first.return_value = fake_existing_entry  # MovieList query

        # Mock the query method on db to return the appropriate query object
        self.db.query.side_effect = [fake_query_list, fake_query_movie, fake_query_movie_list]

        # Call the function under test
        result = add_movie_to_list(self.db, user_email=self.user_email, list_name="My List", movie_id=1)

        # Assert that the result is None because the movie is already in the list
        self.assertIsNone(result)

        # Check that the expected queries were executed
        self.db.query.assert_any_call(ListType)
        self.db.query.assert_any_call(Movie)
        self.db.query.assert_any_call(MovieList)

        
    def test_get_all_lists_with_movies(self):
        """Test retrieving all lists with their movies."""
        # Mock a fake list with the correct attributes
        fake_list = ListType(id=1, name="My List", created_by_user_email=self.user_email)
        
        # Mock related objects for genres and cast members
        fake_genre = Genre(id=1, type="Action")
        fake_cast_member = CastMember(id=1, name="John Doe")
        
        # Mock a fake movie with relationships properly set up
        fake_movie = Movie(
            id=1,
            title="Test Movie",
            description="A great movie",
            director="Director",
            country="Country",
            release_date="2024-01-01",
            rating=4.5,
            rating_count=10,
            likes=5,
            genres=[fake_genre],  # Assign list of Genre objects
            cast_members=[fake_cast_member]  # Assign list of CastMember objects
        )

        # Mock the MovieList relationship, associating the movie with the list
        fake_movie_list = MovieList(list_type_id=fake_list.id, movie_id=fake_movie.id)
        
        # Now, you need to mock the MovieList in the query result
        # Mock the database query behavior for list with movies
        self.db.query.return_value.filter.return_value.all.side_effect = [[fake_list]]
        self.db.query.return_value.filter.return_value.all.return_value = [fake_list]

        # You would also want to mock the join with Movie and its relationships
        self.db.query.return_value.join.return_value.filter.return_value.all.side_effect = [[fake_movie]]
        
        # Call the function to test
        result = get_all_lists_with_movies(self.db, user_email=self.user_email)
        
        # Assertions to verify the results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["list_name"], "My List")
        self.assertEqual(len(result[0]["movies"]), 1)
        self.assertEqual(result[0]["movies"][0]["title"], "Test Movie")

    def test_delete_list_by_name(self):
        """Test deleting a list by name."""
        fake_list = ListType(id=1, name="My List", created_by_user_email=self.user_email)
        fake_movie_list = MovieList(id=1, list_type_id=1, movie_id=1)
        self.db.query.return_value.filter.return_value.first.side_effect = [fake_list, fake_movie_list]

        delete_list_by_name(self.db, user_email=self.user_email, list_name="My List")

        self.db.delete.assert_called()
        self.db.commit.assert_called_once()

    def test_remove_movie_from_list_by_email(self):
        """Test removing a movie from a user's list."""
        fake_list = ListType(id=1, name="My List", created_by_user_email=self.user_email)
        fake_movie_entry = MovieList(list_type_id=1, movie_id=1)

        self.db.query.return_value.filter.return_value.first.side_effect = [fake_list, fake_movie_entry]

        result = remove_movie_from_list_by_email(self.db, user_email=self.user_email, list_name="My List", movie_id=1)

        self.assertIsNotNone(result)
        self.db.delete.assert_called_once()
        self.db.commit.assert_called_once()

    def test_delete_movie_links(self):
        """Test deleting all links to a movie."""
        fake_movie = Movie(id=1, title="Movie Title")
        fake_movie_link = MovieList(list_type_id=1, movie_id=1)

        self.db.get.return_value = fake_movie
        self.db.execute.return_value.scalars.return_value.all.return_value = [fake_movie_link]

        result = delete_movie_links(self.db, movie_id=1)

        self.assertTrue(result)
        self.db.delete.assert_called()
