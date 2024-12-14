import unittest
from datetime import datetime
from sqlmodel import create_engine, Session, SQLModel
from app.models.comments_model import Thread, Comment, ReportStatus
from app.models.movie_models import Movie
from app.models.user_models import User
from app.crud.comments_crud import (
    create_thread,
    create_comment,
    get_threads_by_movie,
    get_comments_by_thread,
    get_comments_reported,
    get_comments_banned,
    get_comments_reported_with_user,
    get_comments_reported_by_user,
    update_comment_text,
    update_comment_status_with_user,
    delete_comment,
    delete_thread,
    get_comments_by_user,
    get_comments,
    get_reported_comments_ordered,
    delete_reported_comment

)

# Initialize test database (SQLite in-memory)
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=False)

# Create tables
SQLModel.metadata.create_all(engine)

class TestCommentThreadCRUD(unittest.TestCase):

    def setUp(self):
        # Start a new session before each test
        self.db = Session(engine)
        # Create test data
        movie = Movie(title="Test Movie")

        # Use this hashed_password while creating users
        user1 = User(email="user1@example.com", hashed_password="hashed_password", is_active=True, is_admin=False)
        user2 = User(email="user2@example.com", hashed_password="hashed_password", is_active=True, is_admin=False)

        self.db.add_all([movie, user1, user2])
        self.db.commit()

    def tearDown(self):
        # Close the db after each test
        self.db.rollback()
        self.db.query(Movie).delete()
        self.db.query(User).delete()
        self.db.query(Thread).delete()
        self.db.query(Comment).delete()
        self.db.commit()
        #self.db.close()

    def test_create_thread(self):
        thread = create_thread(self.db, movie_id=1)
        self.assertIsNotNone(thread.id)
        self.assertEqual(thread.movie_id, 1)

    def test_create_comment(self):
        thread = create_thread(self.db, movie_id=1)
        comment = create_comment(self.db, thread_id=thread.id, user_id=1, text="Test comment")
        self.assertIsNotNone(comment.id)
        self.assertEqual(comment.text, "Test comment")
        self.assertEqual(comment.thread_id, thread.id)

    def test_get_threads_by_movie(self):
        create_thread(self.db, movie_id=1)
        threads = get_threads_by_movie(self.db, movie_id=1)
        self.assertEqual(len(threads), 1)

    def test_get_comments_by_thread(self):
        thread = create_thread(self.db, movie_id=1)
        create_comment(self.db, thread_id=thread.id, user_id=1, text="Comment 1")
        create_comment(self.db, thread_id=thread.id, user_id=2, text="Comment 2")
        comments = get_comments_by_thread(self.db, thread_id=thread.id)
        self.assertEqual(len(comments), 2)

    def test_update_comment_text(self):
        thread = create_thread(self.db, movie_id=1)
        comment = create_comment(self.db, thread_id=thread.id, user_id=1, text="Original text")
        updated_comment = update_comment_text(self.db, comment_id=comment.id, text="Updated text")
        self.assertEqual(updated_comment.text, "Updated text")

    def test_get_comments_reported(self):
        thread = create_thread(self.db, movie_id=1)
        create_comment(self.db, thread_id=thread.id, user_id=1, text="Comment 1")
        reported_comment = create_comment(self.db, thread_id=thread.id, user_id=2, text="Reported comment")
        updated_comment = update_comment_status_with_user(
            self.db, comment_id=reported_comment.id, reported=ReportStatus.REPORTED, user_id=2
        )
        reported_comments = get_comments_reported(self.db)
        self.assertEqual(len(reported_comments), 1)

    def test_delete_comment(self):
        thread = create_thread(self.db, movie_id=1)
        comment = create_comment(self.db, thread_id=thread.id, user_id=1, text="Comment to delete")
        deleted = delete_comment(self.db, comment_id=comment.id)
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get(Comment, comment.id))

    def test_delete_non_comment(self):
        deleted = delete_comment(self.db, comment_id=-1)
        self.assertFalse(deleted)

    def test_delete_thread(self):
        thread = create_thread(self.db, movie_id=1)
        create_comment(self.db, thread_id=thread.id, user_id=1, text="Comment in thread")
        deleted = delete_thread(self.db, movie_id=thread.id)
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get(Thread, thread.id))

    def test_update_comment_status_with_user(self):
        thread = create_thread(self.db, movie_id=1)
        comment = create_comment(self.db, thread_id=thread.id, user_id=1, text="Comment to update status")
        updated_comment = update_comment_status_with_user(
            self.db, comment_id=comment.id, reported=ReportStatus.BANNED, user_id=2
        )
        self.assertEqual(updated_comment.reported, ReportStatus.BANNED)

    def test_update_non_comment_status_with_user(self):
        with self.assertRaises(ValueError) as context:
            update_comment_status_with_user(
                self.db, comment_id=-1, reported=ReportStatus.BANNED, user_id=2
            )
        self.assertEqual(str(context.exception), "Comment not found")

    def test_get_comments_banned(self):
        thread = create_thread(self.db, movie_id=1)
        create_comment(self.db, thread_id=thread.id, user_id=1, text="Clean comment")
        banned_comment = create_comment(self.db, thread_id=thread.id, user_id=2, text="Banned comment")
        updated_comment = update_comment_status_with_user(
            self.db, comment_id=banned_comment.id, reported=ReportStatus.BANNED, user_id=2
        )
        banned_comments = get_comments_banned(self.db)
        self.assertEqual(len(banned_comments), 1)
    
    def test_get_comments_by_user(self):
        thread = create_thread(self.db, movie_id=1)
        create_comment(self.db, thread_id=thread.id, user_id=1, text="User 1 Comment 1")
        create_comment(self.db, thread_id=thread.id, user_id=2, text="User 2 Comment 1")
        comments = get_comments_by_user(self.db, user_id=1)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].text, "User 1 Comment 1")
    
    def test_get_comments(self):
        thread = create_thread(self.db, movie_id=1)
        create_comment(self.db, thread_id=thread.id, user_id=1, text="Comment 1")
        create_comment(self.db, thread_id=thread.id, user_id=2, text="Comment 2")
        comments = get_comments(self.db)
        self.assertEqual(len(comments), 2)

    def test_get_comments_reported_with_user(self):
        thread = create_thread(self.db, movie_id=1)
        comment1 = create_comment(self.db, thread_id=thread.id, user_id=1, text="Reported by User 1")
        updated_comment = update_comment_status_with_user(
            self.db, comment_id=comment1.id, reported=ReportStatus.REPORTED, user_id=2
        )
        comments = get_comments_reported_with_user(self.db, user_id=1)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].text, "Reported by User 1")

    def test_get_comments_reported_by_user(self):
        thread = create_thread(self.db, movie_id=1)
        comment1 = create_comment(self.db, thread_id=thread.id, user_id=2, text="Comment reported by User 1")
        updated_comment = update_comment_status_with_user(
            self.db, comment_id=comment1.id, reported=ReportStatus.REPORTED, user_id=1
        )
        comments = get_comments_reported_by_user(self.db, user_id=1)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].text, "Comment reported by User 1")

    def test_get_reported_comments_ordered(self):
        thread = create_thread(self.db, movie_id=1)
        comment1 = create_comment(self.db, thread_id=thread.id, user_id=1, text="Reported Comment 1")
        comment2 = create_comment(self.db, thread_id=thread.id, user_id=2, text="Reported Comment 2")
        updated_comment = update_comment_status_with_user(
            self.db, comment_id=comment2.id, reported=ReportStatus.BANNED, user_id=2
        )
        updated_comment = update_comment_status_with_user(
            self.db, comment_id=comment1.id, reported=ReportStatus.REPORTED, user_id=1
        )
        comment1.created_at = datetime(2023, 1, 1, 12, 0, 0)  # Older
        comment2.created_at = datetime(2023, 1, 2, 12, 0, 0)  # Newer
        self.db.commit()
        
        # Test ordering by date (default)
        comments = get_reported_comments_ordered(self.db, order_by="date")
        self.assertEqual(len(comments), 2)
        self.assertGreater(comments[0].created_at, comments[1].created_at)

        # Test ordering by user
        comments = get_reported_comments_ordered(self.db, order_by="user")
        self.assertEqual(comments[0].user_id, 1)

        # Test ordering by status
        comments = get_reported_comments_ordered(self.db, order_by="status")
        self.assertEqual(comments[0].reported, ReportStatus.REPORTED)

    def test_delete_reported_comment(self):
        thread = create_thread(self.db, movie_id=1)
        reported_comment = create_comment(self.db, thread_id=thread.id, user_id=1, text="Reported Comment")
        updated_comment = update_comment_status_with_user(
            self.db, comment_id=reported_comment.id, reported=ReportStatus.REPORTED, user_id=1
        )
        deleted = delete_reported_comment(self.db, comment_id=reported_comment.id)
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get(Comment, reported_comment.id))

    def test_delete_non_reported_comment(self):
        thread = create_thread(self.db, movie_id=1)
        clean_comment = create_comment(self.db, thread_id=thread.id, user_id=1, text="Clean Comment")
        updated_comment = update_comment_status_with_user(
            self.db, comment_id=clean_comment.id, reported=ReportStatus.CLEAN, user_id=1
        )
        with self.assertRaises(ValueError) as context:
            delete_reported_comment(self.db, comment_id=clean_comment.id)
        self.assertEqual(str(context.exception), f"Comment with ID {clean_comment.id} is not reported.")

    def test_delete_non_existent_comment(self):
        with self.assertRaises(ValueError) as context:
            delete_reported_comment(self.db, comment_id=-1)
        self.assertEqual(str(context.exception), "Comment with ID -1 not found.")