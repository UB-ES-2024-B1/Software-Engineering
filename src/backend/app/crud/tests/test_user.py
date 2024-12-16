import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.crud.user_crud import get_followers, get_followed_users, follow_user, unfollow_user, create_user, get_users, get_user, get_user_by_email, delete_user, delete_user_by_email, update_user, update_password, update_user_by_email, get_user_by_username
from app.models.user_models import User, UserOut, Follow

class TestUserCRUD(unittest.TestCase):
    def setUp(self):
        """Set up the mock database session."""
        self.db = MagicMock(Session)
        self.fake_user_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'hashed_password': 'hashed_password',
            'is_admin': False
        }
        self.followed_user = User(**self.fake_user_data)
        self.fake_user_data2 = {            
            'id':'21',
            'full_name': 'John Doe2',
            'email': 'john2@example.com',
            'hashed_password': 'hashed_password',
            'is_admin': False
        }
        self.follower_user = User(**self.fake_user_data2)
        self.fake_user_data3 = {
            'id':'20',
            'full_name': 'John Doe3',
            'email': 'john3@example.com',
            'hashed_password': 'hashed_password',
            'is_admin': False
        }
        self.user3 = User(**self.fake_user_data3)

        self.follower_id = self.follower_user.id  
        self.followed_id = self.followed_user.id

        # Create a Follow object to mock the existing follow relationship
        self.follow = Follow(follower_id=self.follower_id, followed_id=self.followed_id)

    def test_create_user(self):
        """Test the create_user function."""
        self.db.add.return_value = None
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.followed_user

        result = create_user(self.db, **self.fake_user_data)
        
        self.assertEqual(result.full_name, 'John Doe')
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()

    def test_get_users(self):
        """Test the get_users function."""
        self.db.query.return_value.offset.return_value.limit.return_value.all.return_value = [self.followed_user]

        result = get_users(self.db, skip=0, limit=10)

        self.assertEqual(len(result), 1)
        self.db.query.return_value.offset.return_value.limit.return_value.all.assert_called_once()

    def test_get_user(self):
        """Test the get_user function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.followed_user

        result = get_user(self.db, user_id=1)

        self.assertEqual(result, self.followed_user)
        self.db.query.return_value.filter.return_value.first.assert_called_once()

    def test_get_user_by_email(self):
        """Test the get_user_by_email function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.followed_user

        result = get_user_by_email(self.db, email="john@example.com")

        self.assertEqual(result, self.followed_user)
        self.db.query.return_value.filter.return_value.first.assert_called_once()

    def test_get_user_by_username(self):
        """Test the get_user_by_email function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.followed_user

        result = get_user_by_username(self.db, "John Doe")

        self.assertEqual(result, self.followed_user)
        self.db.query.return_value.filter.return_value.first.assert_called_once()

    def test_delete_user(self):
        """Test the delete_user function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.followed_user
        self.db.delete.return_value = None
        self.db.commit.return_value = None

        result = delete_user(self.db, user_id=1)

        self.assertTrue(result)
        self.db.delete.assert_called_once()
        self.db.commit.assert_called_once()

    def test_delete_user_not_found(self):
        """Test deleting a user that does not exist."""
        self.db.query.return_value.filter.return_value.first.return_value = None

        result = delete_user(self.db, user_id=999)

        self.assertFalse(result)

    def test_delete_user_by_email(self):
        """Test the delete_user_by_email function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.followed_user
        self.db.delete.return_value = None
        self.db.commit.return_value = None

        result = delete_user_by_email(self.db, user_email="john@example.com")

        self.assertTrue(result)
        self.db.delete.assert_called_once()
        self.db.commit.assert_called_once()

    def test_delete_non_user_by_email(self):
        """Test deleting a user that does not exist by email."""
        self.db.query.return_value.filter.return_value.first.return_value = None

        result = delete_user_by_email(self.db, user_email="nonexistent@example.com")
        self.assertFalse(result)

        self.db.query.return_value.filter.return_value.first.assert_called_once_with()

    def test_update_user(self):
        """Test the update_user function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.followed_user
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.followed_user

        user_data = {'full_name': 'Jane Doe'}
        updated_user = update_user(self.db, user_id=1, user_data=user_data)

        self.assertEqual(updated_user.full_name, 'Jane Doe')
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_non_user(self):
        """Test updating a user that does not exist by email."""
        self.db.query.return_value.filter.return_value.first.return_value = None
        
        user_data = {'full_name': 'Jane Doe'}
        updated_user = update_user(self.db, user_id=1, user_data=user_data)
        self.assertFalse(updated_user)

        self.db.query.return_value.filter.return_value.first.assert_called_once_with()

    def test_update_password(self):
        """Test the update_password function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.followed_user
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.followed_user

        new_password = 'new_hashed_password'
        updated_user = update_password(self.db, user_id=1, new_password=new_password)

        self.assertEqual(updated_user.hashed_password, 'new_hashed_password')
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_password_non_user(self):
        """Test updating password of user that does not exist by email."""
        self.db.query.return_value.filter.return_value.first.return_value = None
                
        new_password = 'new_hashed_password'
        updated_user = update_password(self.db, user_id=1, new_password=new_password)
        self.assertFalse(updated_user)

        self.db.query.return_value.filter.return_value.first.assert_called_once_with()

    def test_update_user_by_email(self):
        """Test the update_user_by_email function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.followed_user
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.followed_user

        user_data = {'full_name': 'Updated Name'}
        updated_user = update_user_by_email(self.db, email="john@example.com", user_data=user_data)

        self.assertEqual(updated_user.full_name, 'Updated Name')
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_non_user_by_email(self):
        """Test updating a user that does not exist by email."""
        self.db.query.return_value.filter.return_value.first.return_value = None
                
        user_data = {'full_name': 'Updated Name'}
        updated_user = update_user_by_email(self.db, email="john@example.com", user_data=user_data)
        self.assertFalse(updated_user)

        self.db.query.return_value.filter.return_value.first.assert_called_once_with()

    def test_follow_user(self):
        """Test the follow_user function when the follow relationship doesn't exist."""
        # Mock the query for the User table to return self.user3
        self.db.query.return_value.filter.return_value.first.side_effect = [
            self.user3,  # First query for the User table returns the user
            None         # Second query for the Follow table returns None
        ]

        # Mock the Follow object creation
        new_follow = Follow(follower_id=self.follower_id, followed_id=self.user3.id)
        self.db.refresh.return_value = new_follow  # Simulate refresh returning the new Follow object

        # Call the function to follow the user
        result = follow_user(self.db, self.follower_id, self.user3.id)
        
        # Assert the result is the existing Follow object
        self.assertEqual(result.followed_id, self.user3.id)
        self.assertEqual(result.follower_id, self.follower_id)

        # Ensure the new Follow object was added, committed, and refreshed
        self.db.add.assert_called_once_with(new_follow)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(new_follow)

    def test_follow_non_user(self):
        """Test the follow_user function when the follow relationship doesn't exist."""

        # Simulate the followed user not existing in the database (this should return None)
        self.db.query.return_value.filter.return_value.first.return_value = None  # No followed user found
        
        # Try to follow the user (the function should return None since the followed user doesn't exist)
        result = follow_user(self.db, self.follower_id, 99999)
        
        # Assert that the result is None, as the followed user does not exist
        self.assertIsNone(result)  # Make sure the result is None
        
        # Ensure that db.query was called with the expected followed_id to check user existence
        self.db.query.return_value.filter.return_value.first.assert_called_with()

    def test_follow_user_existing(self):
        """Test the follow_user function when the follow relationship already exists."""
        # Mock the case where the follow relationship already exists
        self.db.query.return_value.filter.return_value.first.return_value = self.follow

        # Call the function to follow the user
        result = follow_user(self.db, self.follower_id, self.followed_id)

        # Assert the result is the existing Follow object
        self.assertEqual(result.follower_id, self.follower_id)
        self.assertEqual(result.followed_id, self.followed_id)

        # Ensure that no new Follow object is added
        self.db.add.assert_not_called()
        self.db.commit.assert_not_called()
        self.db.refresh.assert_not_called()

    def test_unfollow_user(self):
        """Test the unfollow_user function when the follow relationship exists."""
        # Mock the case where the follow relationship exists
        self.db.query.return_value.filter.return_value.first.return_value = self.follow

        # Call the function to unfollow the user
        result = unfollow_user(self.db, self.follower_id, self.followed_id)

        # Assert the result is True, indicating successful unfollow
        self.assertTrue(result)

        # Ensure the correct database methods are called to delete the follow
        self.db.delete.assert_called_once_with(self.follow)
        self.db.commit.assert_called_once()

    def test_unfollow_user_not_found(self):
        """Test the unfollow_user function when the follow relationship does not exist."""
        # Mock the case where no follow relationship exists
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Call the function to unfollow the user
        result = unfollow_user(self.db, self.follower_id, self.followed_id)

        # Assert the result is False, indicating no follow to delete
        self.assertFalse(result)

        # Ensure that no delete operation is performed
        self.db.delete.assert_not_called()
        self.db.commit.assert_not_called()

    def test_get_followers(self):
        """Test the get_followers function."""
        # Mock the query to return a list of followers for a user
        self.db.query.return_value.join.return_value.filter.return_value.all.return_value = [self.follower_user]
        
        # Call the function to get followers for user with id = 2
        result = get_followers(self.db, user_id=self.followed_user.id)

        # Assert that the result contains the follower user (John Doe2)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].full_name, "John Doe2")

        # Ensure the query was called with correct join and filter
        self.db.query.return_value.join.return_value.filter.return_value.all.assert_called_once()

    def test_get_followers_non_user(self):
        """Test the get_followers function when the follow user doesn't exist."""

        # Simulate the followed user not existing in the database (this should return None)
        self.db.query.return_value.filter.return_value.first.return_value = None  # No followed user found
        
        # Try to follow the user (the function should return None since the followed user doesn't exist)
        result = get_followers(self.db, 99999)
        
        # Assert that the result is None, as the followed user does not exist
        self.assertIsNone(result)  # Make sure the result is None
        
        # Ensure that db.query was called with the expected followed_id to check user existence
        self.db.query.return_value.filter.return_value.first.assert_called_with()

    def test_get_followed_users(self):
        """Test the get_followed_users function."""
        # Mock the query to return a list of followed users for a user
        self.db.query.return_value.join.return_value.filter.return_value.all.return_value = [self.followed_user]
        
        # Call the function to get followed users for user with id = 3
        result = get_followed_users(self.db, user_id=self.follower_user.id)

        # Assert that the result contains the followed user (John Doe)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].full_name, "John Doe")

        # Ensure the query was called with correct join and filter
        self.db.query.return_value.join.return_value.filter.return_value.all.assert_called_once()

    def test_get_followed_non_user(self):
        """Test the get_followers function when the follow user doesn't exist."""

        # Simulate the followed user not existing in the database (this should return None)
        self.db.query.return_value.filter.return_value.first.return_value = None  # No followed user found
        
        # Try to follow the user (the function should return None since the followed user doesn't exist)
        result = get_followed_users(self.db, 99999)
        
        # Assert that the result is None, as the followed user does not exist
        self.assertIsNone(result)  # Make sure the result is None
        
        # Ensure that db.query was called with the expected followed_id to check user existence
        self.db.query.return_value.filter.return_value.first.assert_called_with()