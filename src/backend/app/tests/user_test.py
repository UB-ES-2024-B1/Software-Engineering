# backend/app/tests/user_tests.py
from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct

client = TestClient(app)

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
    update_response = client.put(f"/users/email/testuser@example.com", json=update_data)

    # Verify the update was successful
    assert update_response.status_code == 200
    updated_user_data = update_response.json()
    assert updated_user_data["email"] == update_data["email"]
    assert updated_user_data["full_name"] == update_data["full_name"]
    assert updated_user_data["is_active"] == update_data["is_active"]
    assert updated_user_data["is_admin"] == update_data["is_admin"]

# Test to ensure deleted users cannot be retrieved
def test_deleted_user_cannot_be_retrieved():

    # Delete the user
    delete_response = client.delete(f"/users/email/updateduser@example.com")
    assert delete_response.status_code == 200


# Test trying to get a deleted user
def test_get_user_by_email_3():
    # Get the user by ID
    get_response = client.get(f"/users/email/updateduser@example.com")

    assert get_response.status_code == 404