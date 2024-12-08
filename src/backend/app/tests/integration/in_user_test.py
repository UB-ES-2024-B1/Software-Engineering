from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct

client = TestClient(app)


def test_create_two_users_and_get_and_delete():
    # Define two new users
    user1 = {
        "email": "user1@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "User One",
        "password": "password123"
    }
    user2 = {
        "email": "user2@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "User Two",
        "password": "password456"
    }

    # Create the first user
    response1 = client.post("/users/", json=user1)
    assert response1.status_code == 201
    user1_data = response1.json()
    assert user1_data["email"] == user1["email"]
    assert user1_data["full_name"] == user1["full_name"]

    # Create the second user
    response2 = client.post("/users/", json=user2)
    assert response2.status_code == 201
    user2_data = response2.json()
    assert user2_data["email"] == user2["email"]
    assert user2_data["full_name"] == user2["full_name"]

    # Get the first user by email
    get_response1 = client.get(f"/users/email/{user1['email']}")
    assert get_response1.status_code == 200
    retrieved_user1 = get_response1.json()
    assert retrieved_user1["email"] == user1["email"]
    assert retrieved_user1["full_name"] == user1["full_name"]

    # Get the second user by email
    get_response2 = client.get(f"/users/email/{user2['email']}")
    assert get_response2.status_code == 200
    retrieved_user2 = get_response2.json()
    assert retrieved_user2["email"] == user2["email"]
    assert retrieved_user2["full_name"] == user2["full_name"]

    # Get all users
    all_users_response = client.get("/users/")
    assert all_users_response.status_code == 200
    all_users = all_users_response.json()
    assert isinstance(all_users, list)
    # Ensure the two created users are in the list of all users
    emails = [user["email"] for user in all_users]
    assert user1["email"] in emails
    assert user2["email"] in emails

    # Delete the first user
    delete_response1 = client.delete(f"/users/email/{user1['email']}")
    assert delete_response1.status_code == 200

    # Delete the second user
    delete_response2 = client.delete(f"/users/email/{user2['email']}")
    assert delete_response2.status_code == 200

    # Ensure the first user is deleted
    get_response1_after_delete = client.get(f"/users/email/{user1['email']}")
    assert get_response1_after_delete.status_code == 404

    # Ensure the second user is deleted
    get_response2_after_delete = client.get(f"/users/email/{user2['email']}")
    assert get_response2_after_delete.status_code == 404

def test_create_get_update_delete_user():
    # Create a new user
    new_user = {
        "email": "testuser@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "Test User",
        "password": "password123"
    }
    create_response = client.post("/users/", json=new_user)
    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user["email"] == new_user["email"]
    assert created_user["full_name"] == new_user["full_name"]

    # Retrieve the created user by email
    get_response = client.get(f"/users/email/{new_user['email']}")
    assert get_response.status_code == 200
    retrieved_user = get_response.json()
    assert retrieved_user["email"] == new_user["email"]
    assert retrieved_user["full_name"] == new_user["full_name"]

    # Update the user's information
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

    # Retrieve the updated user by the new email
    get_updated_response = client.get(f"/users/email/{updated_user_data['email']}")
    assert get_updated_response.status_code == 200
    updated_retrieved_user = get_updated_response.json()
    assert updated_retrieved_user["email"] == updated_user_data["email"]
    assert updated_retrieved_user["full_name"] == updated_user_data["full_name"]

    # Delete the user
    delete_response = client.delete(f"/users/email/{updated_user_data['email']}")
    assert delete_response.status_code == 200

    # Ensure the user no longer exists
    get_deleted_response = client.get(f"/users/email/{updated_user_data['email']}")
    assert get_deleted_response.status_code == 404

def test_user_creation_retrieval_duplicate_check_and_deletion():
    # Create a new user
    new_user = {
        "email": "testuser@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "Test User",
        "password": "password123"
    }
    create_response = client.post("/users/", json=new_user)
    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user["email"] == new_user["email"]
    assert created_user["full_name"] == new_user["full_name"]

    # Retrieve the created user by email
    get_response = client.get(f"/users/email/{new_user['email']}")
    assert get_response.status_code == 200
    retrieved_user = get_response.json()
    assert retrieved_user["email"] == new_user["email"]
    assert retrieved_user["full_name"] == new_user["full_name"]

    # Try to create the same user again
    duplicate_response = client.post("/users/", json=new_user)
    assert duplicate_response.status_code == 400  # Should return a 400 Bad Request due to duplicate

    # Attempt to retrieve a non-existent user
    non_existent_user_email = "nonexistent@example.com"
    get_non_existent_response = client.get(f"/users/email/{non_existent_user_email}")
    assert get_non_existent_response.status_code == 404  # Should return 404 Not Found

    # Delete the user
    delete_response = client.delete(f"/users/email/{new_user['email']}")
    assert delete_response.status_code == 200

    # Ensure the user no longer exists
    get_deleted_response = client.get(f"/users/email/{new_user['email']}")
    assert get_deleted_response.status_code == 404  # Should return 404 Not Found