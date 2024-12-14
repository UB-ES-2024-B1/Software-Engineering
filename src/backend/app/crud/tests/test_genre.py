import unittest
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from app.models.movie_models import Genre
from app.crud.genre_crud import get_genres

class TestGetGenres(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )

        # Create tables in the in-memory database
        SQLModel.metadata.create_all(self.engine)

        # Create a session for testing
        self.session = Session(self.engine)

        # Populate the database with test data
        self.genres_data = [
            Genre(type="Action"),
            Genre(type="Comedy"),
            Genre(type="Drama"),
            Genre(type="Horror"),
            Genre(type="Sci-Fi"),
        ]
        self.session.add_all(self.genres_data)
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_get_genres_within_limit(self):
        # Test fetching genres with a limit less than the total count
        skip = 0
        limit = 3
        result = get_genres(self.session, skip=skip, limit=limit)

        self.assertEqual(len(result), limit)
        # Ensure the result contains valid Genre objects
        for genre in result:
            self.assertIsInstance(genre, Genre)

    def test_get_genres_with_skip(self):
        # Test fetching genres with a skip and limit
        skip = 2
        limit = 2
        result = get_genres(self.session, skip=skip, limit=limit)

        self.assertEqual(len(result), limit)
        self.assertEqual(result[0].type, self.genres_data[skip].type)

    def test_get_genres_exceeding_limit(self):
        # Test fetching with a limit greater than the total count
        skip = 0
        limit = 10  # Greater than the number of test genres
        result = get_genres(self.session, skip=skip, limit=limit)

        self.assertEqual(len(result), len(self.genres_data))

    def test_get_genres_empty_result(self):
        # Test fetching with a skip that exceeds the total count
        skip = 10
        limit = 5
        result = get_genres(self.session, skip=skip, limit=limit)

        self.assertEqual(len(result), 0)

