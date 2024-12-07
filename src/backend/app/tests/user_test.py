# backend/app/tests/user_tests.py
from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct

client = TestClient(app)

# Test trying to create a user and check it was created and delete it at the end
def test_create_user():
    # New user data
    new_user = {
        "email": "testuser@example.com",
        "is_active": False,
        "is_admin" : False,
        "full_name": "testuser",
        "password": "password123",
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

##### PREMIUM USER TEST
# Test to check if premium status is False by default for new users
def test_default_premium_status():
    new_user = {
        "email": "testpremiumuser@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "Test Premium User",
        "password": "password123"
    }

    # Create the user
    response = client.post("/users/", json=new_user)
    assert response.status_code == 201

    # Verify premium is False by default
    user_data = response.json()
    assert "is_premium" in user_data
    assert user_data["is_premium"] is False

# Test updating a user to premium
def test_update_user_to_premium():
    user_email = "testpremiumuser@example.com"

    # Update the premium status
    response = client.put(f"/users/upgrade_premium/{user_email}")
    assert response.status_code == 200

    # Verify the response message
    response_data = response.json()
    assert response_data["is_premium"] is True

# Test verifying premium status after update
def test_verify_premium_status():
    response = client.get("/users/email/testpremiumuser@example.com")
    assert response.status_code == 200

    # Verify premium status is now True
    user_data = response.json()
    assert user_data["email"] == "testpremiumuser@example.com"
    assert user_data["is_premium"] is True

# Test to downgrade a user account to standard
def test_remove_premium_status():
    """
    Test removing the premium status from a user.
    """
    user_email = "testpremiumuser@example.com"

    # Update the premium status
    response = client.put(f"/users/downgrade_premium/{user_email}")
    assert response.status_code == 200

    # Verify the response message
    response_data = response.json()
    assert response_data["is_premium"] == False

# Test to try to upgrade a non existing email
def test_update_premium_invalid_email():
    """
    Test updating premium status for a non-existent user.
    """
    invalid_email = "invalidemail@example.com"

    # Try to update premium status for a non-existent user
    response = client.put(f"/users/upgrade_premium/{invalid_email}")
    assert response.status_code == 404

# Test to ensure deleted users cannot be upgrade or downgrade
def test_update_downgrade_deleted_user():
    user_email = "testpremiumuser@example.com"
    # Delete the user
    delete_response = client.delete(f"/users/email/{user_email}")
    assert delete_response.status_code == 200

    # Update the premium status
    response = client.put(f"/users/upgrade_premium/{user_email}")
    assert response.status_code == 404

    # Try to update premium status for a non-existent user
    response = client.put(f"/users/downgrade_premium/{user_email}")
    assert response.status_code == 404



##### ADD NEW TYPE LIST FOR PREMIUM USER
# Test adding a list type as a premium user
def test_add_list_type_as_premium_user():
    # Create a premium user
    premium_user = {
        "email": "premiumuser@example.com",
        "is_active": True,
        "is_premium": True,
        "full_name": "Premium User",
        "password": "password123"
    }
    client.post("/users/", json=premium_user)

    # Add a new list type
    list_type_data = {"name": "Watch Again"}
    response = client.post(f"/list-type/{premium_user['email']}/{list_type_data['name']}")

    assert response.status_code == 201
    assert response.json()["name"] == list_type_data["name"]

# Test adding a list type as a non-premium user
def test_add_list_type_as_non_premium_user():
    # Create a non-premium user
    non_premium_user = {
        "email": "nonpremiumuser@example.com",
        "is_active": True,
        "is_premium": False,
        "full_name": "Non-Premium User",
        "password": "password123"
    }
    client.post("/users/", json=non_premium_user)

    # Attempt to add a new list type
    list_type_data = {"name": "Watch Later"}
    response = client.post(f"/list-type/{non_premium_user['email']}/{list_type_data['name']}")

    assert response.status_code == 400
    assert response.json()["detail"] == "User not found or unable to create list"

# Test to add movie id to a list by name
def test_add_movie_to_list_and_get():
    # Create a user and a list
    user_data = {
        "email": "user@example.com", 
        "is_active": True, 
        "is_premium": True, 
        "full_name": "Test User", 
        "password": "password123"
    }
    client.post("/users/", json=user_data)

    list_type_data = {"name": "Watch Again"}
    client.post(f"/list-type/{user_data['email']}/{list_type_data['name']}")

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

    # Get the data of the new movie
    movie_data = client.get(f"/movies/title/{new_movie['title']}").json()
    response2 = client.post(f"/list-type/add-movie/{user_data['email']}/{list_type_data['name']}/{movie_data['id']}")

    assert response2.status_code == 200
    assert response2.json()["movie_id"] == movie_data['id']

     # Get the list of movie names
    response3 = client.get(f"/list-type/movies/{user_data['email']}/{list_type_data['name']}")
    
    assert response3.status_code == 200
    assert response3.json() == ["The Lost City"]  # Expected movie names

# Test adding a non-existing movie to a list
def test_add_non_existing_movie_to_list():
    # Create a user and a list
    user_data = {
        "email": "user2@example.com", 
        "is_active": True, 
        "is_premium": True, 
        "full_name": "Test User 2", 
        "password": "password456"
    }
    client.post("/users/", json=user_data)

    list_type_data = {"name": "To Watch"}
    client.post(f"/list-type/{user_data['email']}/{list_type_data['name']}")

    movie_data = {"movie_id": 9999}  # Assuming movie ID 9999 does not exist
    response = client.post(f"/list-type/add-movie/{user_data['email']}/{list_type_data['name']}/{movie_data['movie_id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}

# Test adding a movie to a non-existing list
def test_add_movie_to_non_existing_list():
    # Create a user
    user_data = {
        "email": "user3@example.com", 
        "is_active": True, 
        "is_premium": True, 
        "full_name": "Test User 3", 
        "password": "password789"
    }
    client.post("/users/", json=user_data)

    movie_data = {"movie_id": 1}  # Assuming movie ID 1 exists
    # Trying to add movie to a non-existing list
    response = client.post(f"/list-type/add-movie/{user_data['email']}/NonExistentList/{movie_data['movie_id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "List not found"}
