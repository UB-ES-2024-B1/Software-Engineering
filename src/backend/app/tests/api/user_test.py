# backend/app/tests/user_tests.py
from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct
from app.models import User

from app.api.dependencies import get_current_user

client = TestClient(app)

# Mock user for authentication
def mock_get_current_user():
    return User(
        id=2,  # Simulate a user with ID 1
        email="authenticated@example.com",
        is_active=True,
        is_admin=False,
        full_name="Authenticated User",
    )

# Override the dependency
app.dependency_overrides[get_current_user] = mock_get_current_user


# Test trying to create a user and check it was created and delete it at the end
def test_create_user():
    # New user data
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

    # Verify that the response content is correct
    response_data = response.json()
    assert response_data["full_name"] == new_user["full_name"]
    assert response_data["email"] == new_user["email"]
    assert "id" in response_data  # Ensure that an id is generated

# Test trying to create a user with same email
def test_create_user_2():
    # New user data
    new_user = {
        "email": "testuser@example.com",
        "is_active": True,
        "is_admin" : False,
        "full_name": "testuser_2",
        "password": "password1"
    }
    
    # Send a POST request to create a new user
    response = client.post("/users/", json=new_user)

    assert response.status_code == 400

# Test to get all users
def test_get_all_users():
    
    response = client.get("/users/")

    # Verify the response status is 200 OK and that there is at least one user
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0  # Ensure there are users in the list

# Test for getting a user by ID
def test_get_user_by_email():
    # Get the user by ID
    get_response = client.get(f"/users/email/testuser@example.com")

    assert get_response.status_code == 200
    get_user_data = get_response.json()
    assert get_user_data["email"] == "testuser@example.com"

# Test to update a user
def test_update_user():
    # Update the user
    update_data = {
        "email": "updateduser@example.com",
        "is_active": False,
        "is_admin": True,
        "full_name": "updateduser"
    }
    update_response = client.put(f"/users/email/testuser@example.com", data=update_data)

    # Verify the update was successful
    assert update_response.status_code == 200
    updated_user_data = update_response.json()
    assert updated_user_data["email"] == update_data["email"]
    assert updated_user_data["full_name"] == update_data["full_name"]
    assert updated_user_data["is_active"] == update_data["is_active"]
    assert updated_user_data["is_admin"] == update_data["is_admin"]

# Test to follow a user
def test_follow_user():
    new_user = {
        "email": "authenticated@example.com",
        "is_active": True,
        "is_admin" : False,
        "full_name": "testuser",
        "password": "password123"
    }
    
    # Send a POST request to create a new user
    response = client.post("/users/", json=new_user)

    # Simulate current user (assumed to be authenticated)
    user_to_follow_id = 1  # Replace with an existing user ID to follow

    response = client.post(f"/users/follow/{user_to_follow_id}", headers={"Authorization": "Bearer mock-token"})

    # Verify response status
    assert response.status_code == 200

    # Verify the structure of the response
    response_data = response.json()
    # Assert correct response structure
    assert response_data["follower_id"] == 2  # Simulated current user ID
    assert response_data["followed_id"] == user_to_follow_id

# Test to get followers of a user
def test_get_followers():
    # Assuming user with ID 1 exists and has followers
    response = client.get("/users/followers/1")

    # Verify response status
    assert response.status_code == 200

    # Verify the structure of the response
    response_data = response.json()
    assert isinstance(response_data, list)  # Should return a list of followers

    if response_data:  # Check first follower if exists
        follower = response_data[0]        
        assert "id" in follower
        assert "email" in follower
        assert "full_name" in follower

# Test to get followed users of a user
def test_get_followed_users():
    # Assuming user with ID 1 exists and follows other users
    response = client.get("/users/followed/2")

    # Verify response status
    assert response.status_code == 200

    # Verify the structure of the response
    response_data = response.json()
    assert isinstance(response_data, list)  # Should return a list of followed users

    if response_data:  # Check first followed user if exists
        followed_user = response_data[0]
        assert "id" in followed_user
        assert "email" in followed_user
        assert "full_name" in followed_user

# Test to unfollow a user
def test_unfollow_user():
    # Simulate current user (assumed to be authenticated)
    user_to_unfollow_id = 1  # Replace with an existing user ID to unfollow

    response = client.post(f"/users/unfollow/{user_to_unfollow_id}", headers={"Authorization": "Bearer mock-token"})

    # Verify response status
    assert response.status_code == 200

    # Verify the structure of the response
    response_data = response.json()
    assert response_data["message"] == "Unfollowed successfully"

# Test error handling when trying to get followers of a nonexistent user
def test_get_followers_nonexistent_user():
    response = client.get("/users/followers/99999")  # Nonexistent user ID

    # Verify response status
    assert response.status_code == 404

    # Verify the error message
    response_data = response.json()
    assert response_data["detail"] == "User not found or has no followers"

# Test error handling when trying to follow a nonexistent user
def test_follow_nonexistent_user():
    response = client.post("/users/follow/99999", headers={"Authorization": "Bearer mock-token"})
  
    # Verify response status
    assert response.status_code == 404

    # Verify the error message
    response_data = response.json()
    assert response_data["detail"] == "User not found"

# Test error handling when trying to unfollow a nonexistent user
def test_unfollow_nonexistent_user():
    response = client.post("/users/unfollow/-1", headers={"Authorization": "Bearer mock-token"})

    # Verify response status
    assert response.status_code == 500

    # Verify the error message
    response_data = response.json()
    assert response_data["detail"] == "400: Unable to unfollow user"

# Test to ensure deleted users cannot be retrieved
def test_deleted_user_cannot_be_retrieved():    
    # Delete the user
    delete_response = client.delete(f"/users/email/updateduser@example.com")
    assert delete_response.status_code == 200
    
    delete_response = client.delete(f"/users/email/authenticated@example.com")
    assert delete_response.status_code == 200
    
    get_response = client.get(f"/users/email/updateduser@example.com")

    assert get_response.status_code == 404