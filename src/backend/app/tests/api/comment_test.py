from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct
from app.api.routes.user_routes import is_admin_user

# Simulate an admin user being authenticated
def mock_is_admin_user():
        return True  
app.dependency_overrides[is_admin_user] = mock_is_admin_user

client = TestClient(app)

# Test cases for Threads endpoints
def test_create_movie_thread():
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

    movie_id = 1
    response = client.post(f"/comments/threads/?movie_id={movie_id}")

    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["movie_id"] == movie_id

def test_get_threads():
    movie_id = 1
    response = client.get(f"/comments/threads/{movie_id}/")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)

# Test cases for Comments endpoints
def test_add_comment():
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
    user_id = response.json()["id"]

    new_comment = {
        "thread_id": 1,
        "user_id": user_id,
        "text": "This is a test comment."
    }

    response = client.post(f"/comments/?thread_id={new_comment['thread_id']}&user_id={new_comment['user_id']}&text={new_comment['text']}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["text"] == new_comment["text"]
    assert response_data["thread_id"] == new_comment["thread_id"]
    assert response_data["user_id"] == new_comment["user_id"]

def test_get_thread_comments():
    thread_id = 1
    response = client.get(f"/comments/threads/{thread_id}/comments/")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)

def test_update_comment_text():
    comment_id = 1
    update_data = {"text": "Updated comment text."}
    response = client.put(f"/comments/{comment_id}/text", json=update_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["text"] == update_data["text"]

def test_update_comment_status():
    comment_id = 1
    update_data = {"reported": "REPORTED"}
    user_id = 1
    response = client.put(f"/comments/{comment_id}/status?user_id={user_id}", json=update_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["reported"] == update_data["reported"]

def test_remove_comment():
    comment_id = 1
    response = client.delete(f"/comments/{comment_id}/")

    assert response.status_code == 204

def test_remove_thread():
    thread_id = 1
    response = client.delete(f"/comments/threads/{thread_id}/")

    assert response.status_code == 204

# Test cases for Reported Comments endpoints
def test_get_reported_comments():
    response = client.get("/comments/reported/")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)

def test_get_reported_comments_by_user():
    user_id = 1
    response = client.get(f"/comments/reported_by_user/{user_id}/")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)

def test_get_banned_comments():
    response = client.get("/comments/banned/")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)

def test_get_reported_comments_ordered_by_date():
    response = client.get("/comments/reported/order_by_date/")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)

def test_get_reported_comments_ordered_by_user():
    response = client.get("/comments/reported/order_by_user/")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)

def test_get_reported_comments_ordered_by_status():
    response = client.get("/comments/reported/order_by_status/")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)

def test_try_comment_deleted_movie():
    response = client.delete("/movies/title/The Lost City")
    assert response.status_code == 200

     # Delete the user
    delete_response = client.delete(f"/users/email/testuser@example.com")
    assert delete_response.status_code == 200
