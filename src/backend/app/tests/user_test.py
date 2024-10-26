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

    # Step 2: Get the user ID from the created user
    user_id = response_data['id']

    # Step 3: Delete the user with DELETE
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200  # Check that deletion was successful
    
    # Check that the user no longer exists
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404  # The user should not exist after deletion

# Test to get all users
def test_get_all_users():
    # Create a user to ensure there are users in the database
    new_user = {
        "email": "testuser1@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "testuser1",
        "password": "password123"
    }
    client.post("/users/", json=new_user)
    
    response = client.get("/users/")

    # Verify the response status is 200 OK and that there is at least one user
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0  # Ensure there are users in the list

# Test for getting a user by ID
def test_get_user_by_id():
    # Create a user for testing
    new_user = {
        "email": "testuser2@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "testuser2",
        "password": "password123"
    }
    response = client.post("/users/", json=new_user)
    response_data = response.json()
    user_id = response_data['id']

    # Get the user by ID
    get_response = client.get(f"/users/{user_id}")

    assert get_response.status_code == 200
    get_user_data = get_response.json()
    assert get_user_data["id"] == user_id
    assert get_user_data["email"] == new_user["email"]

    # Delete the user after the test
    client.delete(f"/users/{user_id}")

# Test to update a user
def test_update_user():
    # Create a user
    new_user = {
        "email": "testuser3@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "testuser3",
        "password": "password123"
    }
    response = client.post("/users/", json=new_user)
    response_data = response.json()
    user_id = response_data['id']

    # Update the user
    update_data = {
        "email": "updateduser@example.com",
        "is_active": False,
        "is_admin": True,
        "full_name": "updateduser"
    }
    update_response = client.put(f"/users/id/{user_id}", json=update_data)

    # Verify the update was successful
    assert update_response.status_code == 200
    updated_user_data = update_response.json()
    assert updated_user_data["email"] == update_data["email"]
    assert updated_user_data["full_name"] == update_data["full_name"]
    assert updated_user_data["is_active"] == update_data["is_active"]
    assert updated_user_data["is_admin"] == update_data["is_admin"]

    # Delete the user after the test
    client.delete(f"/users/{user_id}")

# Test to ensure deleted users cannot be retrieved
def test_deleted_user_cannot_be_retrieved():
    # Create a user to ensure it exists in the database
    new_user = {
        "email": "testuser4@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "testuser4",
        "password": "password123"
    }
    response = client.post("/users/", json=new_user)
    response_data = response.json()
    user_id = response_data['id']

    # Delete the user
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200

    # Attempt to retrieve the user after deletion
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404  # The user should no longer exist


