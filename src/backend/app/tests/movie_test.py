from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct

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
        ]
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

    assert "id" in response_data

# Test to create a movie
def test_create_movie_2():
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
    assert len(response_data) > 0  # Ensure there are users in the list

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

# Test update rating of movie
def test_update_movie_rating_by_title():
    update_data = {"rating": 4.9}
    response = client.put("/movies/The Lost City/rating", json=update_data)
    assert response.status_code == 200

# Test update likes of movie
def test_add_movie_like():
    response = client.put("/movies/The Lost City/like")
    assert response.status_code == 200

    response_data = response.json()    
    # Assuming likes were initially set to 5300
    assert response_data["likes"] == 5301



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

# Test delete movie 
def test_delete_movie():
    response = client.delete("/movies/title/The Lost City")
    assert response.status_code == 200

# Test to get movie by title
def test_get_movie_by_title_2():
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