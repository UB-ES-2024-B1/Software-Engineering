from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct
from app.api.routes.user_routes import is_admin_user

# Simulate an admin user being authenticated
def mock_is_admin_user():
        return True  



client = TestClient(app)

# Test to create, get by ID, get by name, and delete a movie
def test_create_get_delete_movie():
    app.dependency_overrides[is_admin_user] = mock_is_admin_user
    # Create a new movie
    new_movie = {
        "title": "The Forgotten Kingdom",
        "description": "A group of explorers uncover a lost civilization deep in the jungle, filled with mysteries and danger.",
        "director": "Emily Watson",
        "country": "Brazil",
        "release_date": "2024-11-15",
        "rating": 4.8,
        "rating_count": 8000,
        "likes": 3000,
        "genres": [
            "Adventure",
            "Action"
        ],
        "cast_members": [
            "Chris Brown",
            "Anna Lee",
            "Marcus Steele"
        ],
        "image": [
        ],
        "trailer": ""
    }

    # Create the movie
    response = client.post("/movies/", json=new_movie)
    assert response.status_code == 200

    # Verify that the response content is correct
    response_data = response.json()
    assert response_data["title"] == new_movie["title"]
    assert response_data["description"] == new_movie["description"]
    assert response_data["director"] == new_movie["director"]
    assert response_data["country"] == new_movie["country"]
    assert response_data["release_date"] == new_movie["release_date"]
    assert response_data["rating"] == new_movie["rating"]
    assert response_data["rating_count"] == new_movie["rating_count"]
    assert response_data["likes"] == new_movie["likes"]
    assert "id" in response_data

    # Get the created movie ID for future steps
    movie_id = response_data["id"]

    # Get the movie by ID
    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 200
    response_data_by_id = response.json()

    # Verify that the movie fetched by ID matches the original movie
    assert response_data_by_id["id"] == movie_id
    assert response_data_by_id["title"] == new_movie["title"]
    assert response_data_by_id["description"] == new_movie["description"]

    # Get the movie by title
    response = client.get(f"/movies/title/The Forgotten Kingdom")
    assert response.status_code == 200
    response_data_by_title = response.json()

    # Verify that the movie fetched by title matches the original movie
    assert response_data_by_title["title"] == new_movie["title"]
    assert response_data_by_title["description"] == new_movie["description"]

    # Delete the movie
    response = client.delete(f"/movies/title/The Forgotten Kingdom")
    assert response.status_code == 200

    # Verify that the movie was successfully deleted
    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 404  # Movie should not exist anymore

# Test to create an invalid movie, get by name and ID for non-existent movies, and delete a non-existent movie
def test_create_get_delete_invalid_movie():
    app.dependency_overrides[is_admin_user] = mock_is_admin_user
    invalid_movie = {
        "title": "The Lost Temple",  # Title is provided, but missing description, director, etc.
        "rating": 4.5,
        "rating_count": 10000,
        "likes": 3000,
        "genres": ["Adventure"]
    }

    # Try to create the invalid movie
    response = client.post("/movies/", json=invalid_movie)
    assert response.status_code == 422  # Bad Request due to missing required fields

    # Create a new movie
    new_movie = {
        "title": "The Forgotten Kingdom",
        "description": "A group of explorers uncover a lost civilization deep in the jungle, filled with mysteries and danger.",
        "director": "Emily Watson",
        "country": "Brazil",
        "release_date": "2024-11-15",
        "rating": 4.8,
        "rating_count": 8000,
        "likes": 3000,
        "genres": [
            "Adventure",
            "Action"
        ],
        "cast_members": [
            "Chris Brown",
            "Anna Lee",
            "Marcus Steele"
        ],
        "image": [
        ],
        "trailer": ""
    }

    # Create the movie
    response = client.post("/movies/", json=new_movie)
    assert response.status_code == 200

    # Create a new movie
    new_movie = {
        "title": "The Forgotten Kingdom",
        "description": "A renowned archaeologist stumbles upon a hidden city filled with secrets, leading to a thrilling adventure across uncharted lands.",
        "director": "Sarah Connors",
        "country": "United States",
        "release_date": "2024-10-26",
        "rating": 4.2,
        "rating_count": 12500,
        "likes": 5200,
        "genres": ["Adventure", "Thriller"],
        "cast_members": ["John Doe", "Jane Smith", "Mike Johnson"],
        "image": [],
        "trailer": ""
    }

    # Create the movie
    response = client.post("/movies/", json=new_movie)
    assert response.status_code == 400

    # Delete the movie
    response = client.delete(f"/movies/title/The Forgotten Kingdom")
    assert response.status_code == 200

    # Attempt to get a movie by title that doesn't exist
    response = client.get("/movies/title/NonExistentMovie")
    assert response.status_code == 404  # Movie should not exist

    # Attempt to get a movie by ID that doesn't exist
    response = client.get("/movies/9999")  # Assume ID 9999 doesn't exist
    assert response.status_code == 404  # Movie should not exist

    # Attempt to delete a movie that doesn't exist
    response = client.delete("/movies/title/NonExistentMovie")
    assert response.status_code == 404  # Movie should not exist for deletion

# Test to create, get, update, and delete a movie
def test_create_get_update_delete_movie():
    app.dependency_overrides[is_admin_user] = mock_is_admin_user
    # Create a movie
    new_movie = {
        "title": "The Lost City",
        "description": "A renowned archaeologist stumbles upon a hidden city filled with secrets, leading to a thrilling adventure across uncharted lands.",
        "director": "Sarah Connors",
        "country": "United States",
        "release_date": "2024-10-26",
        "rating": 4.2,
        "rating_count": 12500,
        "likes": 5200,
        "genres": ["Adventure", "Thriller"],
        "cast_members": ["John Doe", "Jane Smith", "Mike Johnson"],
        "image": [],
        "trailer": ""
    }

    # Create the movie
    response = client.post("/movies/", json=new_movie)
    assert response.status_code == 200  # Movie created successfully

    # Verify that the movie data is correct
    response_data = response.json()
    assert response_data["title"] == new_movie["title"]
    assert response_data["description"] == new_movie["description"]
    assert response_data["director"] == new_movie["director"]
    assert response_data["country"] == new_movie["country"]
    assert response_data["release_date"] == new_movie["release_date"]
    assert response_data["rating"] == new_movie["rating"]
    assert response_data["rating_count"] == new_movie["rating_count"]
    assert response_data["likes"] == new_movie["likes"]
    assert response_data["trailer"] == new_movie["trailer"]
    assert "id" in response_data  # Ensure the movie has an ID

    movie_id = response_data["id"]  # Save the movie ID for later use

    # Get the movie by title and verify the data
    response = client.get(f"/movies/title/{new_movie['title']}")
    assert response.status_code == 200  # Movie retrieved successfully
    response_data = response.json()

    assert response_data["title"] == new_movie["title"]
    assert response_data["description"] == new_movie["description"]
    assert response_data["director"] == new_movie["director"]
    assert response_data["country"] == new_movie["country"]
    assert response_data["release_date"] == new_movie["release_date"]
    assert response_data["rating"] == new_movie["rating"]
    assert response_data["rating_count"] == new_movie["rating_count"]
    assert response_data["likes"] == new_movie["likes"]

    # Update the movie
    updated_movie = {
        "title": "The Lost City",
        "description": "Updated description with more adventure and action.",
        "director": "Sarah Connors",
        "country": "United States",
        "release_date": "2024-10-26",
        "rating": 4.7,
        "rating_count": 13000,
        "likes": 5400,
        "genres": ["Adventure", "Action"],
        "cast_members": ["John Doe", "Jane Smith", "Mike Johnson", "Anna Lee"],
        "image": [],
        "trailer": "new_trailer_link"
    }

    # Update the movie data
    response = client.put(f"/movies/The Lost City", json=updated_movie)
    assert response.status_code == 200  # Movie updated successfully

    # Verify that the updated movie data is correct
    response_data = response.json()
    assert response_data["title"] == updated_movie["title"]
    assert response_data["description"] == updated_movie["description"]
    assert response_data["director"] == updated_movie["director"]
    assert response_data["country"] == updated_movie["country"]
    assert response_data["release_date"] == updated_movie["release_date"]
    assert response_data["rating"] == updated_movie["rating"]
    assert response_data["rating_count"] == updated_movie["rating_count"]
    assert response_data["likes"] == updated_movie["likes"]
    assert response_data["trailer"] == updated_movie["trailer"]

    # Get the updated movie by title and confirm it has been updated
    response = client.get(f"/movies/title/{updated_movie['title']}")
    assert response.status_code == 200  # Movie retrieved successfully
    response_data = response.json()

    assert response_data["title"] == updated_movie["title"]
    assert response_data["description"] == updated_movie["description"]
    assert response_data["director"] == updated_movie["director"]
    assert response_data["country"] == updated_movie["country"]
    assert response_data["release_date"] == updated_movie["release_date"]
    assert response_data["rating"] == updated_movie["rating"]
    assert response_data["rating_count"] == updated_movie["rating_count"]
    assert response_data["likes"] == updated_movie["likes"]
    assert response_data["trailer"] == updated_movie["trailer"]

    # Delete the movie
    response = client.delete(f"/movies/title/{updated_movie['title']}")
    assert response.status_code == 200  # Movie deleted successfully

    # Verify the movie is deleted
    response = client.get(f"/movies/title/{updated_movie['title']}")
    assert response.status_code == 404  # Movie not found after deletion

# Test to create a couple of movies, get by one genre and by a list of genres, check genres, and delete movies
def test_create_and_get_movies_by_genre():
    app.dependency_overrides[is_admin_user] = mock_is_admin_user
    # Create the first movie with genres
    movie_1 = {
        "title": "The Lost City",
        "description": "A renowned archaeologist stumbles upon a hidden city filled with secrets, leading to a thrilling adventure across uncharted lands.",
        "director": "Sarah Connors",
        "country": "United States",
        "release_date": "2024-10-26",
        "rating": 4.2,
        "rating_count": 12500,
        "likes": 5200,
        "genres": ["Adventure", "Thriller"],
        "cast_members": ["John Doe", "Jane Smith", "Mike Johnson"],
        "image": [],
        "trailer": ""
    }

    response = client.post("/movies/", json=movie_1)
    assert response.status_code == 200
    movie_1_data = response.json()
    
    # Create the second movie with different genres
    movie_2 = {
        "title": "Cyber Odyssey",
        "description": "In a futuristic world, a group of hackers uncover a conspiracy to control the world's digital systems.",
        "director": "Alex Rivera",
        "country": "United States",
        "release_date": "2025-03-14",
        "rating": 4.8,
        "rating_count": 15000,
        "likes": 6400,
        "genres": ["Action", "Science Fiction", "Thriller"],
        "cast_members": ["Sam Clarkson", "Eve Monroe", "Jaxon Lee"],
        "image": [],
        "trailer": ""
    }

    response = client.post("/movies/", json=movie_2)
    assert response.status_code == 200
    movie_2_data = response.json()

    # Get movies by genre "Adventure"
    response = client.get("/movies/genre/Adventure")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    
    # Check if each movie has the genre "Adventure"
    for movie in movies:
        assert "genres" in movie
        assert isinstance(movie["genres"], list)        
        assert any(genre["type"] == "Adventure" for genre in movie["genres"])

    # Get movies by genre "Action"
    response = client.get("/movies/genre/Action")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)

    # Check if each movie has the genre "Action"
    for movie in movies:
        assert "genres" in movie
        assert isinstance(movie["genres"], list)        
        assert any(genre["type"] == "Action" for genre in movie["genres"])

    # Get movies by multiple genres (Adventure, Thriller)
    response = client.get("/movies/genre/list/Adventure,Thriller")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)

    # Check if movies have "Adventure" and "Thriller"
    for movie in movies:        
        assert "genres" in movie
        assert isinstance(movie["genres"], list)
        assert any(genre["type"] == "Thriller" for genre in movie["genres"])
        assert any(genre["type"] == "Adventure" for genre in movie["genres"])

    # Get movies by multiple genres (Action, Science Fiction)
    response = client.get("/movies/genre/list/Action,Science Fiction")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)

    # Check if movies have "Action" and "Science Fiction"
    for movie in movies:        
        assert "genres" in movie
        assert isinstance(movie["genres"], list)
        assert any(genre["type"] == "Science Fiction" for genre in movie["genres"])
        assert any(genre["type"] == "Action" for genre in movie["genres"])

     # 7. Delete the first movie by title
    response = client.delete(f"/movies/title/{movie_1['title']}")
    assert response.status_code == 200

    # Verify that the first movie is deleted
    response = client.get(f"/movies/title/{movie_1['title']}")
    assert response.status_code == 404

    # 8. Delete the second movie by title
    response = client.delete(f"/movies/title/{movie_2['title']}")
    assert response.status_code == 200

    # Verify that the second movie is deleted
    response = client.get(f"/movies/title/{movie_2['title']}")
    assert response.status_code == 404

# Test create a movie, get by release year, and delete the movie
def test_create_get_and_delete_movie_by_year():
    app.dependency_overrides[is_admin_user] = mock_is_admin_user
    # Create a movie with a specific release year
    movie_data = {
        "title": "Future Wars",
        "description": "A dystopian future where humans fight for survival against AI-controlled armies.",
        "director": "Jane Doe",
        "country": "United States",
        "release_date": "2024-05-15",  # Release year 2024
        "rating": 4.6,
        "rating_count": 8000,
        "likes": 3200,
        "genres": ["Action", "Sci-Fi"],
        "cast_members": ["John Dee", "Alice Johnson", "Mike Waters"],
        "image": [],
        "trailer": ""
    }

    # Create the movie
    response = client.post("/movies/", json=movie_data)
    assert response.status_code == 200
    movie_data_response = response.json()
    movie_title = movie_data_response["title"]

    # Get movies by release year 2024
    response = client.get("/movies/release/2024")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    
    # Check if all movies in the list have the release year 2024
    for movie in movies:
        assert "2024" in movie["release_date"]

    # Delete the movie by title
    response = client.delete(f"/movies/title/{movie_title}")
    assert response.status_code == 200

    # Verify that the movie is deleted by trying to get it by title
    response = client.get(f"/movies/title/{movie_title}")
    assert response.status_code == 404

# Test create movies, get by invalid genre and list of invalid genres, and delete the movies
def test_create_get_invalid_genres_and_delete():
    app.dependency_overrides[is_admin_user] = mock_is_admin_user
    # Create two movies with specific genres
    movie_data_1 = {
        "title": "The Space Odyssey",
        "description": "A journey to explore the unknown reaches of space.",
        "director": "Alice Walker",
        "country": "United States",
        "release_date": "2024-07-18",
        "rating": 4.7,
        "rating_count": 15000,
        "likes": 6800,
        "genres": ["Sci-Fi", "Adventure"],
        "cast_members": ["Tom Hanks", "Emma Stone"],
        "image": [],
        "trailer": ""
    }

    movie_data_2 = {
        "title": "The Lost Kingdom",
        "description": "An ancient kingdom hidden beneath the jungle, waiting to be discovered.",
        "director": "John Smith",
        "country": "United States",
        "release_date": "2024-08-22",
        "rating": 4.3,
        "rating_count": 12000,
        "likes": 5000,
        "genres": ["Adventure", "Action"],
        "cast_members": ["Will Smith", "Charlize Theron"],
        "image": [],
        "trailer": ""
    }

    # Create the movies
    response_1 = client.post("/movies/", json=movie_data_1)
    assert response_1.status_code == 200
    movie_data_response_1 = response_1.json()
    movie_title_1 = movie_data_response_1["title"]

    response_2 = client.post("/movies/", json=movie_data_2)
    assert response_2.status_code == 200
    movie_data_response_2 = response_2.json()
    movie_title_2 = movie_data_response_2["title"]

    # Attempt to get movies by an invalid genre ("Fun")
    response_invalid_genre = client.get("/movies/genre/Fun")
    assert response_invalid_genre.status_code == 404

    # Attempt to get movies by an invalid list of genres ("Fantasy,Fun")
    response_invalid_genre_list = client.get("/movies/genre/list/Fantasy,Fun")
    assert response_invalid_genre_list.status_code == 404

    # Delete the movies by title
    response_delete_1 = client.delete(f"/movies/title/{movie_title_1}")
    assert response_delete_1.status_code == 200

    response_delete_2 = client.delete(f"/movies/title/{movie_title_2}")
    assert response_delete_2.status_code == 200

    # Verify that the movies are deleted by trying to get them by title
    response_check_deleted_1 = client.get(f"/movies/title/{movie_title_1}")
    assert response_check_deleted_1.status_code == 404

    response_check_deleted_2 = client.get(f"/movies/title/{movie_title_2}")
    assert response_check_deleted_2.status_code == 404

# Test create a movie, get by invalid release year, and delete the movie
def test_create_get_invalid_year_and_delete():
    app.dependency_overrides[is_admin_user] = mock_is_admin_user

    # Create a movie with a specific release year
    movie_data = {
        "title": "The Future Vision",
        "description": "A futuristic adventure about the implications of technology on society.",
        "director": "Brian Johnson",
        "country": "United States",
        "release_date": "2025-05-10",  # Release year 2025
        "rating": 4.8,
        "rating_count": 16000,
        "likes": 7200,
        "genres": ["Sci-Fi", "Drama"],
        "cast_members": ["Scarlett Johansson", "Chris Hemsworth"],
        "image": [],
        "trailer": ""
    }

    # Create the movie
    response = client.post("/movies/", json=movie_data)
    assert response.status_code == 200
    movie_data_response = response.json()
    movie_title = movie_data_response["title"]

    # Attempt to get movies by an invalid release year 
    response_invalid_year = client.get("/movies/release/2100")
    assert response_invalid_year.status_code == 200
    movies = response_invalid_year.json()
    assert isinstance(movies, list)
    assert len(movies) == 0

    # Delete the movie by title
    response_delete = client.delete(f"/movies/title/{movie_title}")
    assert response_delete.status_code == 200

    # Verify that the movie is deleted by trying to get it by title
    response_check_deleted = client.get(f"/movies/title/{movie_title}")
    assert response_check_deleted.status_code == 404  # Expecting a 404 since the movie should be deleted

# Test to create 6 movies, get related movies for one, and delete all movies
def test_create_get_related_movies_and_delete():
    app.dependency_overrides[is_admin_user] = mock_is_admin_user
    # Movie data for 6 movies
    movie_data = [
        {
            "title": "The Lost City",
            "description": "A renowned archaeologist stumbles upon a hidden city filled with secrets, leading to a thrilling adventure across uncharted lands.",
            "director": "Sarah Connors",
            "country": "United States",
            "release_date": "2024-10-26",
            "rating": 4.2,
            "rating_count": 12500,
            "likes": 5200,
            "genres": ["Adventure", "Thriller"],
            "cast_members": ["John Doe", "Jane Smith", "Mike Johnson"],
            "image": [],
            "trailer": ""
        },
        {
            "title": "The Hidden Valley",
            "description": "A group of explorers discovers a hidden valley where they must survive against ancient forces.",
            "director": "Sarah Connors",
            "country": "United States",
            "release_date": "2023-05-14",
            "rating": 4.1,
            "rating_count": 11000,
            "likes": 5300,
            "genres": ["Adventure", "Action"],
            "cast_members": ["John Doe", "Tom Hanks", "Emily Stone"],
            "image": [],
            "trailer": ""
        },
        {
            "title": "City of Shadows",
            "description": "In a city ravaged by corruption, one man must uncover a conspiracy that could destroy the world.",
            "director": "John Wills",
            "country": "United Kingdom",
            "release_date": "2025-01-12",
            "rating": 4.5,
            "rating_count": 15000,
            "likes": 6000,
            "genres": ["Thriller", "Drama"],
            "cast_members": ["Chris Hemsworth", "Hugh Jackman", "Scarlett Johansson"],
            "image": [],
            "trailer": ""
        },
        {
            "title": "Adventurers of the Sea",
            "description": "A daring crew sails into uncharted waters, facing mythical beasts and fierce challenges.",
            "director": "Mary Lee",
            "country": "Australia",
            "release_date": "2022-07-19",
            "rating": 4.3,
            "rating_count": 13000,
            "likes": 5900,
            "genres": ["Adventure", "Fantasy"],
            "cast_members": ["Chris Pratt", "Emma Stone", "Will Smith"],
            "image": [],
            "trailer": ""
        },
        {
            "title": "The Last Battle",
            "description": "The final confrontation between good and evil, set in a post-apocalyptic world.",
            "director": "Robert Brown",
            "country": "Canada",
            "release_date": "2024-03-15",
            "rating": 4.7,
            "rating_count": 17000,
            "likes": 7400,
            "genres": ["Action", "Adventure"],
            "cast_members": ["Ryan Reynolds", "Dwayne Johnson", "Zoe Saldana"],
            "image": [],
            "trailer": ""
        },
        {
            "title": "Mystery of the Haunted Mansion",
            "description": "A group of friends investigates the mystery of an ancient mansion plagued by supernatural occurrences.",
            "director": "Anna Fields",
            "country": "United States",
            "release_date": "2023-11-22",
            "rating": 4.4,
            "rating_count": 14000,
            "likes": 6600,
            "genres": ["Thriller", "Horror"],
            "cast_members": ["Tom Cruise", "Meryl Streep", "Johnny Depp"],
            "image": [],
            "trailer": ""
        }
    ]

    # Create all 6 movies
    created_movie_titles = []
    for movie in movie_data:
        response = client.post("/movies/", json=movie)
        assert response.status_code == 200
        created_movie_titles.append(movie["title"])

    # Test to get related movies by title
    response_related_movies = client.get("/movies/sorted/related_movies/The Lost City")
    assert response_related_movies.status_code == 200

    related_movies = response_related_movies.json()
    assert isinstance(related_movies, list)
    
    # Check that no more than 5 related movies are returned
    assert len(related_movies) <= 60
    
    # Validate structure and relation to "The Lost City"
    for movie in related_movies:
        assert "title" in movie
        assert "genres" in movie
        assert "cast_members" in movie
        assert "director" in movie
        # Ensure it's not the same movie as "The Lost City"
        assert movie["title"] != "The Lost City"

    # Optional: Verify that genres, cast, or director match the target movie
    target_movie = {
        "genres": ["Adventure", "Thriller"],
        "cast_members": ["John Doe", "Jane Smith", "Mike Johnson"],
        "director": "Sarah Connors"
    }

    # For each movie in related movies, compare the genres and cast members
    for movie in related_movies[:5]:
        movie_genres = set(genre['type'] for genre in movie['genres'])
        movie_cast = set(cast_member['name'] for cast_member in movie['cast_members'])
        
        # Check for shared genres
        shared_genres = movie_genres.intersection(target_movie['genres'])
        shared_cast = movie_cast.intersection(target_movie['cast_members'])

        director_match = movie["director"] == target_movie["director"]

        # At least one attribute should match to be considered related
        assert len(shared_genres) > 0 or len(shared_cast) > 0 or director_match
    
    # Delete all created movies
    for title in created_movie_titles:
        response_delete = client.delete(f"/movies/title/{title}")
        assert response_delete.status_code == 200

        # Verify that the movie is deleted by trying to get it by title
        response_check_deleted = client.get(f"/movies/title/{title}")
        assert response_check_deleted.status_code == 404  # Expecting a 404 since the movie should be deleted

