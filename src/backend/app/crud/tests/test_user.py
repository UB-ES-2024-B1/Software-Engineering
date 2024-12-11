import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.crud.user_crud import create_user, get_users, get_user, get_user_by_email, delete_user, delete_user_by_email, update_user, update_password, update_user_by_email
from app.models.user_models import User, UserOut

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
        self.user = User(**self.fake_user_data)

    def test_create_user(self):
        """Test the create_user function."""
        self.db.add.return_value = None
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.user

        result = create_user(self.db, **self.fake_user_data)

        self.assertEqual(result.full_name, 'John Doe')
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()

    def test_get_users(self):
        """Test the get_users function."""
        self.db.query.return_value.offset.return_value.limit.return_value.all.return_value = [self.user]

        result = get_users(self.db, skip=0, limit=10)

        self.assertEqual(len(result), 1)
        self.db.query.return_value.offset.return_value.limit.return_value.all.assert_called_once()

    def test_get_user(self):
        """Test the get_user function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.user

        result = get_user(self.db, user_id=1)

        self.assertEqual(result, self.user)
        self.db.query.return_value.filter.return_value.first.assert_called_once()

    def test_get_user_by_email(self):
        """Test the get_user_by_email function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.user

        result = get_user_by_email(self.db, email="john@example.com")

        self.assertEqual(result, self.user)
        self.db.query.return_value.filter.return_value.first.assert_called_once()

    def test_delete_user(self):
        """Test the delete_user function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.user
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
        self.db.query.return_value.filter.return_value.first.return_value = self.user
        self.db.delete.return_value = None
        self.db.commit.return_value = None

        result = delete_user_by_email(self.db, user_email="john@example.com")

        self.assertTrue(result)
        self.db.delete.assert_called_once()
        self.db.commit.assert_called_once()

    def test_update_user(self):
        """Test the update_user function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.user
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.user

        user_data = {'full_name': 'Jane Doe'}
        updated_user = update_user(self.db, user_id=1, user_data=user_data)

        self.assertEqual(updated_user.full_name, 'Jane Doe')
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_password(self):
        """Test the update_password function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.user
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.user

        new_password = 'new_hashed_password'
        updated_user = update_password(self.db, user_id=1, new_password=new_password)

        self.assertEqual(updated_user.hashed_password, 'new_hashed_password')
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_user_by_email(self):
        """Test the update_user_by_email function."""
        self.db.query.return_value.filter.return_value.first.return_value = self.user
        self.db.commit.return_value = None
        self.db.refresh.return_value = self.user

        user_data = {'full_name': 'Updated Name'}
        updated_user = update_user_by_email(self.db, email="john@example.com", user_data=user_data)

        self.assertEqual(updated_user.full_name, 'Updated Name')
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
