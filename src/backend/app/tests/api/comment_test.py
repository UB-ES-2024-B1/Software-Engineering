from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct
from app.api.routes.user_routes import is_admin_user

# Simulate an admin user being authenticated (override the dependency)
def mock_is_admin_user():
    return True  # Mock the user as an admin
app.dependency_overrides[is_admin_user] = mock_is_admin_user

client = TestClient(app)

# Test to create a movie thread and add a comment
def test_create_thread_and_comment():
    # Step 1: Create a movie
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
        "image": [],
        "trailer": ""
    }

    response = client.post("/movies/", json=new_movie)
    assert response.status_code == 200
    movie_data = response.json()
    assert "id" in movie_data
    movie_id = movie_data["id"]  # Capture the movie ID to use in the thread creation

    # Step 2: Create a thread for the movie
    response = client.post(f"/comments/threads/?movie_id={movie_id}")
    assert response.status_code == 200
    thread_data = response.json()
    assert "id" in thread_data
    thread_id = thread_data["id"]  # Capture the thread ID to use for commenting

    new_user = {
        "email": "testuser@example.com",
        "is_active": True,
        "is_admin" : False,
        "full_name": "testuser",
        "password": "password123"
    }
    
    # Send a POST request to create a new user
    response = client.post("/users/", json=new_user)

    # Assert that the response status is 201 CREATED
    assert response.status_code == 201

    # Step 3: Add a comment to the thread
    new_comment = {
        "thread_id": thread_id,
        "user_id": response.json()['id'],  # Assuming user_id = 1, adjust if necessary
        "text": "This is an amazing movie!"
    }

    response = client.post(f"/comments/?thread_id={new_comment['thread_id']}&user_id={new_comment['user_id']}&text={new_comment['text']}", json=new_comment)
    assert response.status_code == 200
    comment_data = response.json()
    assert "id" in comment_data
    assert comment_data["text"] == "This is an amazing movie!"  # Verify the comment text

def test_ban_comment_not_found():
    """
    Test banning a non-existing comment.
    """
    response = client.delete("/movies/title/The Lost City")
    assert response.status_code == 200

    delete_response = client.delete(f"/users/email/testuser@example.com")
    assert delete_response.status_code == 200

    # Call the API to ban a comment that doesn't exist
    response = client.put("/comments/reported_to_banned/999/")  # Using a non-existing ID

    # Assert the response
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}
