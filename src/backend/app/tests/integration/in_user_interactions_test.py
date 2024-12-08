from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct
from app.api.routes.user_routes import is_admin_user

# Simulate an admin user being authenticated
def mock_is_admin_user():
        return True  
app.dependency_overrides[is_admin_user] = mock_is_admin_user


client = TestClient(app)

# Test creating a movie, liking it, and then deleting the movie
def test_create_get_like_and_delete_movie():
    # New user and movie data
    new_user = {
        "email": "testusermovie@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "testusermovie",
        "password": "password123"
    }

    new_movie = {
        "title": "Test Film for Like",
        "description": "A story of adventure and excitement.",
        "director": "TBA",
        "country": "USA",
        "release_date": "2024-03-08",
        "rating": 4.0,
        "rating_count": 30000,
        "likes": 0,
        "genres": ["Action", "Adventure"],
        "cast_members": ["Actor 1", "Actor 2"],
        "image": [],
        "trailer": ""
    }

    # Create the user and movie
    response1 = client.post("/users/", json=new_user)
    response2 = client.post("/movies/", json=new_movie)
    
    # Assert creation was successful
    assert response1.status_code == 201
    assert response2.status_code == 200

    # Get the movie by ID
    movie_id = response2.json()["id"]
    get_response = client.get(f"/movies/{movie_id}")
    assert get_response.status_code == 200
    movie_data = get_response.json()
    assert movie_data["title"] == new_movie["title"]

    # Like the movie with user_id 1
    user_id = 1
    like_response = client.post(f"/movies/like/{movie_id}/{user_id}")
    
    # Assert the like was successful
    assert like_response.status_code == 200
    like_data = like_response.json()
    assert like_data["liked"] == True  

    # Get the movie again to check the updated like count
    get_response_after_like = client.get(f"/movies/{movie_id}")
    assert get_response_after_like.status_code == 200
    movie_data_after_like = get_response_after_like.json()
    assert movie_data_after_like["likes"] == 1  # Verify the like count

    # Delete the movie
    delete_response = client.delete(f"/movies/title/Test Film for Like")
    assert delete_response.status_code == 200
    
    # Try to get the deleted movie
    get_response_after_delete = client.get(f"/movies/{movie_id}")
    assert get_response_after_delete.status_code == 404  # Movie should not be found

    # Delete the  user
    delete_response1 = client.delete(f"/users/email/{new_user['email']}")
    assert delete_response1.status_code == 200
    
    # Ensure the user is deleted
    get_response1_after_delete = client.get(f"/users/email/{new_user['email']}")
    assert get_response1_after_delete.status_code == 404

# Test creating a movie, rating it, and then deleting the movie
def test_create_get_rate_and_delete_movie():
    # New user and movie data
    new_user = {
        "email": "testuserrating@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "testuserrating",
        "password": "password123"
    }

    new_movie = {
        "title": "Test Film for Rating",
        "description": "A story of adventure and excitement.",
        "director": "TBA",
        "country": "USA",
        "release_date": "2024-03-08",
        "rating": 4.0,
        "rating_count": 30000,
        "likes": 0,
        "genres": ["Action", "Adventure"],
        "cast_members": ["Actor 1", "Actor 2"],
        "image": [],
        "trailer": ""
    }

    # Create the user and movie
    response1 = client.post("/users/", json=new_user)
    response2 = client.post("/movies/", json=new_movie)
    
    # Assert creation was successful
    assert response1.status_code == 201
    assert response2.status_code == 200

    # Get the movie by ID
    movie_id = response2.json()["id"]
    get_response = client.get(f"/movies/{movie_id}")
    assert get_response.status_code == 200
    movie_data = get_response.json()
    assert movie_data["title"] == new_movie["title"]

    # Rate the movie with user_id 1 and rating of 4.5
    user_id = 1
    rating = 4.5
    rate_response = client.post(f"/movies/rate/{movie_id}/{user_id}/{rating}")
    
    # Assert the rating was successful
    assert rate_response.status_code == 200
    rate_data = rate_response.json()
    assert rate_data["rating"] == rating  # Verify the rating matches the one provided

    # Get the movie again to check the updated rating
    get_response_after_rate = client.get(f"/movies/{movie_id}")
    assert get_response_after_rate.status_code == 200
    movie_data_after_rate = get_response_after_rate.json()
    assert movie_data_after_rate["rating_count"] == new_movie["rating_count"]+1  # Verify the rating was updated correctly

    # Delete the movie
    delete_response = client.delete(f"/movies/title/Test Film for Rating")
    assert delete_response.status_code == 200
    
    # Try to get the deleted movie
    get_response_after_delete = client.get(f"/movies/{movie_id}")
    assert get_response_after_delete.status_code == 404  # Movie should not be found

    # Delete the  user
    delete_response1 = client.delete(f"/users/email/{new_user['email']}")
    assert delete_response1.status_code == 200
    
    # Ensure the user is deleted
    get_response1_after_delete = client.get(f"/users/email/{new_user['email']}")
    assert get_response1_after_delete.status_code == 404

def test_create_get_invalid_rate_and_invalid_like_movie():
    # New user and movie data
    new_user = {
        "email": "testuserrating@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "testuserrating",
        "password": "password123"
    }

    new_movie = {
        "title": "Test Film",
        "description": "A story of adventure and excitement.",
        "director": "TBA",
        "country": "USA",
        "release_date": "2024-03-08",
        "rating": 4.0,
        "rating_count": 30000,
        "likes": 0,
        "genres": ["Action", "Adventure"],
        "cast_members": ["Actor 1", "Actor 2"],
        "image": [],
        "trailer": ""
    }

    # Create the user and movie
    response1 = client.post("/users/", json=new_user)
    response2 = client.post("/movies/", json=new_movie)
    
    # Assert creation was successful
    assert response1.status_code == 201
    assert response2.status_code == 200

    # Get the movie by ID
    movie_id = response2.json()["id"]
    get_response = client.get(f"/movies/{movie_id}")
    assert get_response.status_code == 200
    movie_data = get_response.json()
    assert movie_data["title"] == new_movie["title"]

    # Try to rate the movie with an invalid rating 
    user_id = 1
    invalid_rating = 6.0  # Invalid rating value
    rate_response = client.post(f"/movies/rate/{movie_id}/{user_id}/{invalid_rating}")
    
    # Assert the rating failed and returned the correct error status
    assert rate_response.status_code == 400  # Expecting Bad Request due to invalid rating

    user_id = 1
    invalid_rating = -1  # Invalid rating value
    rate_response = client.post(f"/movies/rate/{movie_id}/{user_id}/{invalid_rating}")
    
    # Assert the rating failed and returned the correct error status
    assert rate_response.status_code == 400  # Expecting Bad Request due to invalid rating

    # Try to rate the movie with an invalid user ID 
    user_id = 9999999
    rating = 4  # Invalid rating value
    rate_response = client.post(f"/movies/rate/{movie_id}/{user_id}/{rating}")
    
    # Assert the rating failed and returned the correct error status
    assert rate_response.status_code == 404  # Expecting Bad Request due to invalid rating

    # Try to rate the movie with an invalid movie ID 
    user_id = 1
    rating = 4  # Invalid rating value
    rate_response = client.post(f"/movies/rate/9999/{user_id}/{rating}")
    
    # Assert the rating failed and returned the correct error status
    assert rate_response.status_code == 404  # Expecting Bad Request due to invalid rating

    # Try to like the movie with an invalid user ID 
    invalid_user_id = 99999  # Invalid user ID
    like_response = client.post(f"/movies/like/{movie_id}/{invalid_user_id}")
    
    # Assert the like failed due to invalid user ID
    assert like_response.status_code == 404  # Expecting Not Found error (User not found)

    # Try to like the movie with an invalid movie
    invalid_user_id = 1
    like_response = client.post(f"/movies/like/99999/{invalid_user_id}")
    
    # Assert the like failed due to invalid user ID
    assert like_response.status_code == 404

    # Delete the movie
    delete_response = client.delete(f"/movies/title/Test Film")
    assert delete_response.status_code == 200
    
    # Try to get the deleted movie
    get_response_after_delete = client.get(f"/movies/{movie_id}")
    assert get_response_after_delete.status_code == 404  # Movie should not be found

    # Delete the  user
    delete_response1 = client.delete(f"/users/email/{new_user['email']}")
    assert delete_response1.status_code == 200
    
    # Ensure the user is deleted
    get_response1_after_delete = client.get(f"/users/email/{new_user['email']}")
    assert get_response1_after_delete.status_code == 404

def test_create_user_and_movie_add_to_wishlist_and_delete_movie():
    # New user and movie data
    new_user = {
        "email": "testuserwishlist@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "testuserwishlist",
        "password": "password123"
    }

    new_movie = {
        "title": "Test Film for Wishlist",
        "description": "A thrilling journey to the unknown.",
        "director": "Director Name",
        "country": "USA",
        "release_date": "2024-05-01",
        "rating": 4.0,
        "rating_count": 5000,
        "likes": 100,
        "genres": ["Action", "Thriller"],
        "cast_members": ["Actor 1", "Actor 2"],
        "image": [],
        "trailer": ""
    }

    # Create the user
    response1 = client.post("/users/", json=new_user)
    assert response1.status_code == 201  # Assert user creation successful

    # Create the movie
    response2 = client.post("/movies/", json=new_movie)
    assert response2.status_code == 200  # Assert movie creation successful

    # Get the movie and user IDs
    movie_id = response2.json()["id"]
    user_id = response1.json()["id"]

    # Add movie to the user's wishlist
    response3 = client.post(f"/movies/wish/{movie_id}/{user_id}")
    assert response3.status_code == 200  # Assert wishlist addition successful
    response_data = response3.json()
    assert response_data["wished"] == True  # Verify the movie is wished

    # Check if the movie is in the user's wishlist (optional check)
    wishlist_response = client.get(f"/movies/wished_list/{user_id}")
    assert wishlist_response.status_code == 200
    wishlist_data = wishlist_response.json()
    assert any(movie == "Test Film for Wishlist" for movie in wishlist_data)

    # Now delete the movie by title
    delete_response = client.delete(f"/movies/title/Test Film for Wishlist")
    assert delete_response.status_code == 200  # Assert movie deletion successful

    # Try to get the deleted movie
    get_response_after_delete = client.get(f"/movies/{movie_id}")
    assert get_response_after_delete.status_code == 404  # Movie should not be found

    # Delete the  user
    delete_response1 = client.delete(f"/users/email/{new_user['email']}")
    assert delete_response1.status_code == 200
    
    # Ensure the user is deleted
    get_response1_after_delete = client.get(f"/users/email/{new_user['email']}")
    assert get_response1_after_delete.status_code == 404

def test_create_user_and_invalid_add_to_wishlist():
    # New user and movie data
    new_user = {
        "email": "testuserwishlist@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "testuserwishlist",
        "password": "password123"
    }

    new_movie = {
        "title": "Test Film for Wishlist",
        "description": "A thrilling journey to the unknown.",
        "director": "Director Name",
        "country": "USA",
        "release_date": "2024-05-01",
        "rating": 4.0,
        "rating_count": 5000,
        "likes": 100,
        "genres": ["Action", "Thriller"],
        "cast_members": ["Actor 1", "Actor 2"],
        "image": [],
        "trailer": ""
    }

    # Create the user
    response1 = client.post("/users/", json=new_user)
    assert response1.status_code == 201  # Assert user creation successful

    # Create the movie
    response2 = client.post("/movies/", json=new_movie)
    assert response2.status_code == 200  # Assert movie creation successful

    # Get the movie ID (we'll use an invalid movie ID later)
    movie_id = response2.json()["id"]
    user_id = response1.json()["id"]

    # Now simulate an invalid add-to-wishlist by using an invalid movie ID (non-existent movie ID)
    invalid_user_id = 99999  # Using a random invalid user ID
    response3 = client.post(f"/movies/wish/{movie_id}/{invalid_user_id}")
    
    # Assert that the response returns an error because the movie doesn't exist
    assert response3.status_code == 404  # Movie not found (expected error)

    # Now simulate an invalid add-to-wishlist by using an invalid movie ID (non-existent movie ID)
    invalid_movie_id = 99999  # Using a random invalid movie ID
    response3 = client.post(f"/movies/wish/{invalid_movie_id}/{user_id}")
    
    # Assert that the response returns an error because the movie doesn't exist
    assert response3.status_code == 404  # Movie not found (expected error)

    # Ensure the user’s wishlist was not affected
    wishlist_response = client.get(f"/movies/wished_list/{user_id}")
    assert wishlist_response.status_code == 200
    wishlist_data = wishlist_response.json()
    assert len(wishlist_data) == 0  # Ensure the wishlist is still empty, since the add failed

    # Now delete the movie by title
    delete_response = client.delete(f"/movies/title/Test Film for Wishlist")
    assert delete_response.status_code == 200  # Assert movie deletion successful

    # Try to get the deleted movie
    get_response_after_delete = client.get(f"/movies/{movie_id}")
    assert get_response_after_delete.status_code == 404  # Movie should not be found

    # Delete the  user
    delete_response1 = client.delete(f"/users/email/{new_user['email']}")
    assert delete_response1.status_code == 200
    
    # Ensure the user is deleted
    get_response1_after_delete = client.get(f"/users/email/{new_user['email']}")
    assert get_response1_after_delete.status_code == 404

# Can't delete movie before delte threads and comments
def test_create_movie_user_comment_and_get_comment_status():
    # New user data
    new_user = {
        "email": "testusercomments@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "testusercomments",
        "password": "password123"
    }

    # New movie data
    new_movie = {
        "title": "Test Film for Comments",
        "description": "A thrilling journey to the unknown.",
        "director": "Director Name",
        "country": "USA",
        "release_date": "2024-05-01",
        "rating": 4.0,
        "rating_count": 5000,
        "likes": 100,
        "genres": ["Action", "Thriller"],
        "cast_members": ["Actor 1", "Actor 2"],
        "image": [],
        "trailer": ""
    }

    # Create the user
    response1 = client.post("/users/", json=new_user)  # Assumes /users/ is the correct route for user creation
    assert response1.status_code == 201  # Assert user creation successful

    # Create the movie
    response2 = client.post("/movies/", json=new_movie)  # Assumes /movies/ is the correct route for movie creation
    assert response2.status_code == 200  # Assert movie creation successful

    # Get movie id and user id
    movie_id = response2.json()["id"]
    user_id = response1.json()["id"]

    # Create a movie thread for the movie, passing movie_id as a query parameter
    response3 = client.post(f"/comments/threads/?movie_id={movie_id}")
    assert response3.status_code == 200  # Assert thread creation successful
    thread_id = response3.json()["id"]

    # Add a comment to the movie thread
    comment_text = "This movie is amazing!"
    response4 = client.post(f"/comments/?thread_id={thread_id}&user_id={user_id}&text={comment_text}")
    assert response4.status_code == 200  # Assert comment creation successful
    comment_id = response4.json()["id"]

    # Verify the comment after the update
    response5 = client.get(f"/comments/threads/{thread_id}/comments/")  # Fetch updated comment by ID
    assert response5.status_code == 200  # Assert comment retrieval after status update
    updated_comment_data = response5.json()
    assert any(comment["text"] == comment_text for comment in updated_comment_data)

    # DELETE the comment
    response8 = client.delete(f"/comments/{comment_id}")
    assert response8.status_code == 204  # Assert comment deletion successful

    # Verify the comment delete
    response5 = client.get(f"/comments/threads/{thread_id}/comments")  # Fetch updated comment by ID
    assert response5.status_code == 200  # Assert comment retrieval after status update
    updated_comment_data = response5.json()
    assert all(comment["text"] != comment_text for comment in updated_comment_data)

    # DELETE the thread
    response10 = client.delete(f"/comments/threads/{thread_id}")
    assert response10.status_code == 204  # Assert thread deletion successful

    # Verify the thread delete
    response5 = client.get(f"/comments/threads/{thread_id}")  # Fetch updated comment by ID
    assert response5.status_code == 200
    updated_comment_data = response5.json()
    assert len(updated_comment_data) <= 0

    # Now delete the movie by title
    delete_response = client.delete(f"/movies/title/Test Film for Comments")
    assert delete_response.status_code == 200  # Assert movie deletion successful

    # Try to get the deleted movie
    get_response_after_delete = client.get(f"/movies/{movie_id}")
    assert get_response_after_delete.status_code == 404  # Movie should not be found

    # Delete the  user
    delete_response1 = client.delete(f"/users/email/{new_user['email']}")
    assert delete_response1.status_code == 200
    
    # Ensure the user is deleted
    get_response1_after_delete = client.get(f"/users/email/{new_user['email']}")
    assert get_response1_after_delete.status_code == 404

# No check if thread, comment or movie exist
def test_create_movie_user_comment_invalid():
    # New movie data
    new_movie = {
        "title": "Test Film for Comments",
        "description": "A thrilling journey to the unknown.",
        "director": "Director Name",
        "country": "USA",
        "release_date": "2024-05-01",
        "rating": 4.0,
        "rating_count": 5000,
        "likes": 100,
        "genres": ["Action", "Thriller"],
        "cast_members": ["Actor 1", "Actor 2"],
        "image": [],
        "trailer": ""
    }

    # Create the movie
    response2 = client.post("/movies/", json=new_movie)  # Assumes /movies/ is the correct route for movie creation
    assert response2.status_code == 200  # Assert movie creation successful

    # Get movie id and user id
    movie_id = response2.json()["id"]

    # Create a movie thread for a non existing movie
    response3 = client.post("/comments/threads/?movie_id=99999")
    assert response3.status_code == 404  # Assert thread creation successful
    
    # Now delete the movie by title
    delete_response = client.delete(f"/movies/title/Test Film for Comments")
    assert delete_response.status_code == 200  # Assert movie deletion successful

    # Try to get the deleted movie
    get_response_after_delete = client.get(f"/movies/{movie_id}")
    assert get_response_after_delete.status_code == 404  # Movie should not be found
