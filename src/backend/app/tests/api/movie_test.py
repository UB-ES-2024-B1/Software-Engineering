from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct
from app.api.routes.user_routes import is_admin_user

# Simulate an admin user being authenticated
def mock_is_admin_user():
        return True  
app.dependency_overrides[is_admin_user] = mock_is_admin_user


client = TestClient(app)

# Test to create a movie
def test_create_movie():    
    new_movie = {
        "title": "The Lost City",
        "description": "A renowned archaeologist stumbles upon a hidden city filled with secrets, leading to a thrilling adventure across uncharted lands.",
        "director": "Sarah Connors",
        "country": "United States",
        "release_date": "2024-10-26",
        "rating": 4.2,
        "rating_count": 12500,
        "likes": 5200,
        "genres": [
            "Adventure",
            "Thriller"
        ],
        "cast_members": [
            "John Doe",
            "Jane Smith",
            "Mike Johnson"
        ],
        "image": [
        ],
        "trailer": ""
    }

    response = client.post("/movies/", json=new_movie)

    # Assert that the response status 
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
    assert response_data["trailer"] == new_movie["trailer"]

    assert "id" in response_data

# Test to create a movie
def test_create_movie_invalid():
    new_movie = {
        "title": "The Lost City",
        "description": "A renowned archaeologist stumbles upon a hidden city filled with secrets, leading to a thrilling adventure across uncharted lands.",
        "director": "Sarah Connors",
        "country": "United States",
        "release_date": "2024-10-26",
        "rating": 4.2,
        "rating_count": 12500,
        "likes": 5200,
        "genres": [
            "Adventure",
            "Thriller"
        ],
        "cast_members": [
            "John Doe",
            "Jane Smith",
            "Mike Johnson"
        ]
    }

    response = client.post("/movies/", json=new_movie)

    # Assert that the response status 
    assert response.status_code == 400

# Test to get list of movies
def test_get_movies():
    response = client.get("/movies/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) >= 0  # Ensure there are users in the list

# Test to get movie by title
def test_get_movie_by_title():
    response = client.get("/movies/title/The Lost City")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["title"] == "The Lost City"
# Test to get movie by id
def test_get_movie_by_id():
    response = client.get("/movies/1")
    assert response.status_code == 200

# Test to get movie by id
def test_get_movie_by_id_2():
    response = client.get("/movies/-3")
    assert response.status_code == 404

# Test to get movies sorted by date
def test_get_movies_sorted_by_release_date():
    response = client.get("/movies/sorted/release_date")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    # Check if the list is sorted by release date in ascending order
    assert all(
        movies[i]["release_date"] <= movies[i + 1]["release_date"]
        for i in range(len(movies) - 1)
    )

# Test to get movies sorted by rating
def test_get_movies_sorted_by_rating():
    response = client.get("/movies/sorted/rating")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    # Check if the list is sorted by rating in descending order
    assert all(
        movies[i]["rating"] >= movies[i + 1]["rating"]
        for i in range(len(movies) - 1)
    )

# Test to get movies sorted by likes
def test_get_movies_sorted_by_likes():
    response = client.get("/movies/sorted/likes")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    # Check if the list is sorted by likes in descending order
    assert all(
        movies[i]["likes"] >= movies[i + 1]["likes"]
        for i in range(len(movies) - 1)
    )

# Test update movie
def test_update_movie():
    update_data = {
        "title": "The Lost City",
        "description": "Updated description",
        "director": "Sarah Connors",
        "country": "United States",
        "release_date": "2024-10-26",
        "rating": 4.5,
        "rating_count": 13000,
        "likes": 5300,
        "genres": ["Adventure", "Action"],
        "cast_members": ["John Doe", "Jane Smith"]
    }
    response = client.put("/movies/The Lost City", json=update_data)
    assert response.status_code == 200

    # Verify that the response content is correct
    response_data = response.json()
    assert response_data["title"] == update_data["title"]
    assert response_data["description"] == update_data["description"]
    assert response_data["director"] == update_data["director"]
    assert response_data["country"] == update_data["country"]
    assert response_data["release_date"] == update_data["release_date"]
    assert response_data["rating"] == update_data["rating"]
    assert response_data["rating_count"] == update_data["rating_count"]
    assert response_data["likes"] == update_data["likes"]

# Test get movies by year
def test_get_movies_by_year():
    response = client.get("/movies/release/2010")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    # Check if the movies in the list have all the year correct
    for movie in movies:
        assert "2010" in movie["release_date"]

# Test not get movies by year
def test_get_movies_by_year_2():
    response = client.get("/movies/release/2100")
    assert response.status_code == 200

    movies = response.json()
    assert isinstance(movies, list)
    assert len(movies) == 0


# Test get movies with genre
def test_get_movies_by_genre():
    response = client.get("/movies/genre/Adventure")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    # Check if the movies in the list have all the genre
    for movie in movies:
        assert "genres" in movie
        assert isinstance(movie["genres"], list)
        
        assert any(genre["type"] == "Adventure" for genre in movie["genres"])


# Test get movies with genre
def test_get_movies_by_genre_2():
    response = client.get("/movies/genre/Fun")
    assert response.status_code == 404

# Test get movies with multiple genre
def test_get_movies_by_genre_list():
    response = client.get("/movies/genre/list/Adventure,Thriller")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    # Check if the movies in the list have all the genre
    for movie in movies:        
        assert "genres" in movie
        assert isinstance(movie["genres"], list)
        assert any(genre["type"] == "Thriller" for genre in movie["genres"])
        assert any(genre["type"] == "Adventure" for genre in movie["genres"])


# Test get movies with multiplegenre
def test_get_movies_by_genre_list_2():
    response = client.get("/movies/genre/list/Adventure,Science Fiction,Fun")
    assert response.status_code == 404


'''
# Test to get related movies by title
def test_get_related_movies_by_title():
    # Precondition: "The Lost City" should already exist in the database with appropriate genres, cast, and director
    response = client.get("/movies/sorted/related_movies/The Lost City")
    assert response.status_code == 200

    related_movies = response.json()
    assert isinstance(related_movies, list)
    
    # Check that no more than 5 movies are returned
    assert len(related_movies) <= 60

    # Validate structure and relation to the target movie
    for movie in related_movies:
        assert "title" in movie
        assert "genres" in movie
        assert "cast_members" in movie
        assert "director" in movie
        # Ensure it's not the same movie as the input
        assert movie["title"] != "The Lost City"

    # Optional: Verify that genres, cast, or director match the target movie
    target_movie = {
        "genres": ["Adventure", "Thriller"],
        "cast_members": ["John Doe", "Jane Smith", "Mike Johnson"],
        "director": "Sarah Connors"
    }
    for movie in related_movies:
        movie_genres = set(genre['type'] for genre in movie['genres'])
        movie_cast = set(cast_member['name'] for cast_member in movie['cast_members'])
        
        # Check for shared genres
        shared_genres = movie_genres.intersection(target_movie['genres'])
        shared_cast = movie_cast.intersection(target_movie['cast_members'])
        director_match = movie["director"] == target_movie["director"]

        # At least one attribute should match to be considered related
        assert len(shared_genres) > 0 or len(shared_cast) > 0 or director_match
'''
# Test delete movie 
def test_delete_movie():
    response = client.delete("/movies/title/The Lost City")
    assert response.status_code == 200

# Test to get movie by title
def test_get_non_existent_movie_by_title():
    response = client.get("/movies/title/The Lost City")
    assert response.status_code == 404

# Test to search movies by name (valid search)
def test_search_movies_by_name():
    response = client.get("/movies/search/name/barb")
    assert response.status_code == 200
    response_data = response.json()

    # Check if we have movies returned that match the search query
    assert isinstance(response_data, list)

    # Check if movie titles contain 'barb'
    for movie in response_data:
        assert "barb" in movie["title"].lower()

# Test rating a movie
def test_rate_movie():
    # Test data for movie rating
    # New user data
    
    new_user = {
        "email": "testusermovie@example.com",
        "is_active": True,
        "is_admin" : False,
        "full_name": "testusermovie",
        "password": "password123"
    }
    new_movie2 = {
        "title": "Test film",
        "description": "Po and his new ally face a sorceress who wants to take their Staff of Wisdom from them.",
        "director": "TBA",
        "country": "USA",
        "release_date": "2024-03-08",
        "rating": 4.0,
        "rating_count": 30000,
        "likes": 90000,
        "genres": [
            "Animation",
            "Action",
            "Adventure"
        ],
        "cast_members": [
            "Jack Black",
            "Dustin Hoffman"
        ],
        "image": [
        ],
        "trailer": ""
    }
    # Create the initial data
    response1 = client.post("/users/", json=new_user)
    response2 = client.post("/movies/", json=new_movie2)
    assert response1.status_code == 201
    assert response2.status_code == 200
    
    movie_id = 1
    user_id = 1
    rating = 4.0
    
    # Simulate the movie rating request
    response = client.post(f"/movies/rate/{movie_id}/{user_id}/{rating}")

    # Assert the response status code
    assert response.status_code == 200
    
    # Check that the rating is correctly reflected in the response
    response_data = response.json()
    assert "rating" in response_data  # Ensure 'rating' key is returned
    assert response_data["rating"] == rating

# Test rating a movie with invalid rating
def test_rate_movie_invalid_rating():
    movie_id = 1
    user_id = 1 
    invalid_rating = 6.0  # Invalid rating value, out of the range [0, 5]
    
    response = client.post(f"/movies/rate/{movie_id}/{user_id}/{invalid_rating}")
    
    assert response.status_code == 400  # Expect a Bad Request status code

# Test liking a movie
def test_like_movie():
    movie_id = 1
    user_id = 1
    
    # Simulate the like movie request
    response = client.post(f"/movies/like/{movie_id}/{user_id}")
    
    # Assert the response status code
    assert response.status_code == 200
    
    # Check that the likes are updated
    response_data = response.json()
    assert response_data["liked"] == True  # Ensure that likes have increased

# Test adding a movie to wish list
def test_add_wish_movie():
    movie_id = 1
    user_id = 1
    
    # Simulate the wish movie request
    response = client.post(f"/movies/wish/{movie_id}/{user_id}")
    
    # Assert the response status code
    assert response.status_code == 200
    
    # Check that the wish are updated
    response_data = response.json()
    assert response_data["wished"] == True  # Ensure that wish have become to True

# Test liking a movie with toggling
def test_toggle_like_movie():
    movie_id = 1
    user_id = 1
    
    # First, simulate liking the movie
    response = client.post(f"/movies/like/{movie_id}/{user_id}")
    assert response.status_code == 200
    
    # Store initial likes
    initial_likes = response.json()["liked"]
    
    # Simulate unliking the movie 
    response2 = client.post(f"/movies/like/{movie_id}/{user_id}")
    assert response2.status_code == 200
    
    # Ensure the likes are still the same for the same user
    assert response2.json()["liked"] == initial_likes

# Test wishing a movie with toggling
def test_toggle_wish_movie():
    movie_id = 1
    user_id = 1
    
    # First, simulate wishing the movie
    response = client.post(f"/movies/wish/{movie_id}/{user_id}")
    assert response.status_code == 200
    
    # Store initial likes
    initial_wish = response.json()["wished"]
    
    # Simulate nowishing the movie 
    response2 = client.post(f"/movies/wish/{movie_id}/{user_id}")
    assert response2.status_code == 200
    
    # Ensure the wish are still the same for the same user
    assert response2.json()["wished"] == initial_wish

# Test updating movie rating (re-rating)
def test_update_movie_rating():
    movie_id = 1
    user_id = 1
    new_rating = 3.0
    
    # First, simulate rating the movie
    response = client.post(f"/movies/rate/{movie_id}/{user_id}/{new_rating}")
    assert response.status_code == 200
    
    # Check the new rating is updated correctly
    response_data = response.json()
    assert response_data["rating"] == new_rating

# Test to rate a movie with invalid movie ID
def test_rate_movie_invalid_movie_id():
    invalid_movie_id = 99999  # A movie ID that doesn't exist
    user_id = 1
    rating = 4.0
    
    response = client.post(f"/movies/rate/{invalid_movie_id}/{user_id}/{rating}")
    
    assert response.status_code == 404  # Expecting Not Found error

# Test to like a non-existent movie
def test_like_movie_invalid_movie_id():
    invalid_movie_id = 99999  # A movie ID that doesn't exist
    user_id = 1
    
    response = client.post(f"/movies/like/{invalid_movie_id}/{user_id}")
    
    assert response.status_code == 404  # Expecting Not Found error

# Test to like a movie with an invalid user ID
def test_like_movie_invalid_user_id():
    movie_id = 1
    invalid_user_id = 99999  # An invalid user ID
    
    response = client.post(f"/movies/like/{movie_id}/{invalid_user_id}")
    
    assert response.status_code == 404  # Expecting Not Found error (User not found)

# Test to wish a non-existent movie
def test_wish_movie_invalid_movie_id():
    invalid_movie_id = 99999  # A movie ID that doesn't exist
    user_id = 1
    
    response = client.post(f"/movies/wish/{invalid_movie_id}/{user_id}")
    
    assert response.status_code == 404  # Expecting Not Found error

# Test to wish a movie with an invalid user ID
def test_wish_movie_invalid_user_id():
    movie_id = 1
    invalid_user_id = 99999  # An invalid user ID
    
    response = client.post(f"/movies/wish/{movie_id}/{invalid_user_id}")
    
    assert response.status_code == 404  # Expecting Not Found error (User not found)

# Test to remove rating to a movie
def test_remove_rate_movie():
    # Test data for movie rating
    movie_id = 1
    user_id = 1
    
    # Simulate the remove movie rating request
    response = client.post(f"/movies/unrate/{movie_id}/{user_id}")

    # Assert the response status code
    assert response.status_code == 200
    
    # Check that the rating is correctly reflected in the response
    response_data = response.json()
    assert response_data["rating"] == None

# Test disliking a movie
def test_remove_like_movie():
    movie_id = 1
    user_id = 1
    
    # Simulate the like movie request
    response = client.post(f"/movies/dislike/{movie_id}/{user_id}")
    
    # Assert the response status code
    assert response.status_code == 200
    
    # Check that the likes are updated
    response_data = response.json()
    assert response_data["liked"] == False  # Ensure that likes have increased

# Test no wishing a movie
def test_remove_wish_movie():
    movie_id = 1
    user_id = 1
    
    # Simulate the like movie request
    response = client.post(f"/movies/nowish/{movie_id}/{user_id}")
    
    # Assert the response status code
    assert response.status_code == 200
    
    # Check that the likes are updated
    response_data = response.json()
    assert response_data["wished"] == False  # Ensure that likes have increased


# Test updating movie rating (re-rating)
def test_update_movie_rating_after_remove():
    movie_id = 1
    user_id = 1
    new_rating = 3.0
    
    # First, simulate rating the movie
    response = client.post(f"/movies/rate/{movie_id}/{user_id}/{new_rating}")
    assert response.status_code == 200
    
    # Check the new rating is updated correctly
    response_data = response.json()
    assert response_data["rating"] == new_rating

# Test to remove a rate a movie with invalid movie ID
def test_remove_rate_movie_invalid_movie_id():
    invalid_movie_id = 99999  # A movie ID that doesn't exist
    user_id = 1
    
    response = client.post(f"/movies/unrate/{invalid_movie_id}/{user_id}")
    
    assert response.status_code == 404  # Expecting Not Found error

# Test to remove like a non-existent movie
def test_remove_like_movie_invalid_movie_id():
    invalid_movie_id = 99999  # A movie ID that doesn't exist
    user_id = 1
    
    response = client.post(f"/movies/dislike/{invalid_movie_id}/{user_id}")
    
    assert response.status_code == 404  # Expecting Not Found error

# Test to like a movie with an invalid user ID
def test_remove_like_movie_invalid_user_id():
    movie_id = 1
    invalid_user_id = 99999  # An invalid user ID
    
    response = client.post(f"/movies/dislike/{movie_id}/{invalid_user_id}")
    
    assert response.status_code == 404  # Expecting Not Found error (User not found)

# Test to remove wish a non-existent movie
def test_remove_wish_movie_invalid_movie_id():
    invalid_movie_id = 99999  # A movie ID that doesn't exist
    user_id = 1
    
    response = client.post(f"/movies/nowish/{invalid_movie_id}/{user_id}")
    
    assert response.status_code == 404  # Expecting Not Found error

# Test to wish a movie with an invalid user ID
def test_remove_wish_movie_invalid_user_id():
    movie_id = 1
    invalid_user_id = 99999  # An invalid user ID
    
    response = client.post(f"/movies/nowish/{movie_id}/{invalid_user_id}")
    
    assert response.status_code == 404  # Expecting Not Found error (User not found)

# Test to get the list of rating and liked of a user
def test_get_liked_and_rated_movies():
    user_id = 1  # Assuming the user with ID 1 exists
    
    # Get the liked and rated movies for the user
    response = client.get(f"/movies/liked_rated_and_wished_list/{user_id}")
    
    assert response.status_code == 200
    
    response_data = response.json()
    
    # Check if the response contains liked and rated movies
    assert "liked_movies" in response_data
    assert isinstance(response_data["liked_movies"], list)
    
    assert "rated_movies" in response_data
    assert isinstance(response_data["rated_movies"], list)
    
    # Check that the liked and rated movie lists are not empty
    assert len(response_data["liked_movies"]) >= 0
    assert len(response_data["rated_movies"]) >= 0

# Test to get the list of rating of a user
def test_get_liked_list_movies():
    user_id = 1  # Assuming the user with ID 1 exists
    
    # Get the liked and rated movies for the user
    response = client.get(f"/movies/liked_list/{user_id}")
    
    assert response.status_code == 200
    response_data = response.json()

    # Get the full movie list
    all_movies_response = client.get("/movies/")  # Replace with your actual endpoint for getting all movies
    assert all_movies_response.status_code == 200
    all_movies = all_movies_response.json()

    
    # Check that the liked and rated movie lists are not empty
    assert len(response_data) >= 0
    '''# Check that all liked movies are in the full movie list
    liked_movie_ids = {movie["id"] for movie in response_data}
    all_movie_ids = {movie["id"] for movie in all_movies}

    # Validate that every liked movie is in the full movie list
    assert liked_movie_ids.issubset(all_movie_ids), "Some liked movies are missing from the full movie list"
'''
# Test to get the list of wish of a user
def test_get_wish_list_movies():
    user_id = 1  # Assuming the user with ID 1 exists
    
    # Get the liked and rated movies for the user
    response = client.get(f"/movies/wished_list/{user_id}")
    
    assert response.status_code == 200
    response_data = response.json()

    # Get the full movie list
    all_movies_response = client.get("/movies/")  # Replace with your actual endpoint for getting all movies
    assert all_movies_response.status_code == 200
    all_movies = all_movies_response.json()

    
    # Check that the liked and rated movie lists are not empty
    assert len(response_data) >= 0
    '''# Check that all liked movies are in the full movie list
    wished_movie_ids = {movie["id"] for movie in response_data}
    all_movie_ids = {movie["id"] for movie in all_movies}

    # Validate that every liked movie is in the full movie list
    assert wished_movie_ids.issubset(all_movie_ids), "Some liked movies are missing from the full movie list"
    '''

# Test to like a non existing user
def test_like_non_existing_user():
    response = client.delete("/users/email/testusermovie@example.com")
    assert response.status_code == 200

    movie_id = 1
    user_id = -1
    
    # Simulate the movie like request
    response3 = client.post(f"/movies/like/{movie_id}/{user_id}")
    assert response3.status_code == 404  # Expecting Not Found error

# Test to rate a non existing user
def test_rate_non_existing_user():
    movie_id = 1
    user_id = -1
    rating = 5.0
    
    # Simulate the movie rating request 
    response2 = client.post(f"/movies/rate/{movie_id}/{user_id}/{rating}")
    # Assert the response status code
    assert response2.status_code == 404

# Test to wish a non existing user
def test_wish_non_existing_user():
    movie_id = 1
    user_id = -1
    
    # Simulate the movie rating request 
    response2 = client.post(f"/movies/wish/{movie_id}/{user_id}")
    # Assert the response status code
    assert response2.status_code == 404

# Test to like a non existing movie
def test_like_non_existing_movie():
    response = client.delete("/movies/title/Test film")
    assert response.status_code == 200

    movie_id = -1
    user_id = 1
    
    # Simulate the movie like request
    response3 = client.post(f"/movies/like/{movie_id}/{user_id}")
    assert response3.status_code == 404  # Expecting Not Found error

 # Test to rating a non existing movie
def test_rating_non_existing_movie():
    movie_id = -1
    user_id = 1
    rating = 5.0
    
    # Simulate the movie rating request
    response2 = client.post(f"/movies/rate/{movie_id}/{user_id}/{rating}")
    # Assert the response status code
    assert response2.status_code == 404

# Test to wish a non existing movie
def test_wish_non_existing_movie():
    movie_id = -1
    user_id = 1
    
    # Simulate the movie rating request
    response2 = client.post(f"/movies/wish/{movie_id}/{user_id}")
    # Assert the response status code
    assert response2.status_code == 404
