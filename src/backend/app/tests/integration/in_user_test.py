from fastapi.testclient import TestClient
from app.main import app  # Ensure the import is correct
from app.models import User
from app.api.dependencies import get_current_user
from app.api.routes.user_routes import is_admin_user
client = TestClient(app)



# Simulate an admin user being authenticated
def mock_is_admin_user():
        return True  

# Mock user for authentication
def mock_get_current_user(user_id):
    def _mock_user():
        return User(
            id=user_id,
            email="user2test@example.com",
            is_active=True,
            is_admin=False,
            full_name="User Two",
        )
    return _mock_user




def test_create_two_users_and_get_and_delete():
    # Define two new users
    user1 = {
        "email": "user1test@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "User One",
        "password": "password123"
    }
    user2 = {
        "email": "user2test@example.com",
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

def test_user_follow_and_delete():
    # Create the first user
    user_1 = {
        "email": "user1test@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "User One",
        "password": "password123"
    }
    response_1 = client.post("/users/", json=user_1)
    assert response_1.status_code == 201
    user_1_data = response_1.json()
    user_1_id = user_1_data["id"]

    # Create the second user
    user_2 = {
        "email": "user2test@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "User Two",
        "password": "password123"
    }
    response_2 = client.post("/users/", json=user_2)
    assert response_2.status_code == 201
    user_2_data = response_2.json()
    user_2_id = user_2_data["id"]

    # Override the dependency
    app.dependency_overrides[get_current_user] = mock_get_current_user(user_2_id)

    # User 2 follows User 1
    follow_response = client.post(f"/users/follow/{user_1_id}", headers={"Authorization": "Bearer mock-token"})
    assert follow_response.status_code == 200
    follow_data = follow_response.json()
    assert follow_data["follower_id"] == user_2_id
    assert follow_data["followed_id"] == user_1_id

    # Verify User 1's followers
    followers_response = client.get(f"/users/followers/{user_1_id}")
    assert followers_response.status_code == 200
    followers_data = followers_response.json()
    assert len(followers_data) == 1
    assert followers_data[0]["id"] == user_2_id
    assert followers_data[0]["email"] == user_2["email"]

    # Verify User 2's followed users
    followed_response = client.get(f"/users/followed/{user_2_id}")
    assert followed_response.status_code == 200
    followed_data = followed_response.json()
    assert len(followed_data) == 1
    assert followed_data[0]["id"] == user_1_id
    assert followed_data[0]["email"] == user_1["email"]

    # Delete User 1
    delete_user_1 = client.delete(f"/users/email/{user_1['email']}")
    assert delete_user_1.status_code == 200

    # Ensure User 1 cannot be retrieved
    get_deleted_user_1 = client.get(f"/users/email/{user_1['email']}")
    assert get_deleted_user_1.status_code == 404

    # Delete User 2
    delete_user_2 = client.delete(f"/users/email/{user_2['email']}")
    assert delete_user_2.status_code == 200

    # Ensure User 2 cannot be retrieved
    get_deleted_user_2 = client.get(f"/users/email/{user_2['email']}")
    assert get_deleted_user_2.status_code == 404


def test_user_follow_unfollow_and_delete():
    # Create the first user
    user_1 = {
        "email": "user1test@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "User One",
        "password": "password123"
    }
    response_1 = client.post("/users/", json=user_1)
    assert response_1.status_code == 201
    user_1_data = response_1.json()
    user_1_id = user_1_data["id"]

    # Create the second user
    user_2 = {
        "email": "user2test@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "User Two",
        "password": "password123"
    }
    response_2 = client.post("/users/", json=user_2)
    assert response_2.status_code == 201
    user_2_data = response_2.json()
    user_2_id = user_2_data["id"]

    # Override the dependency
    app.dependency_overrides[get_current_user] = mock_get_current_user(user_2_id)

    # User 2 follows User 1
    follow_response = client.post(f"/users/follow/{user_1_id}", headers={"Authorization": "Bearer mock-token"})
    assert follow_response.status_code == 200
    follow_data = follow_response.json()
    assert follow_data["follower_id"] == user_2_id
    assert follow_data["followed_id"] == user_1_id

    response = client.post(f"/users/unfollow/{user_1_id}", headers={"Authorization": "Bearer mock-token"})

    # Verify response status
    assert response.status_code == 200

    # Verify the structure of the response
    response_data = response.json()
    assert response_data["message"] == "Unfollowed successfully"

    # Delete User 1
    delete_user_1 = client.delete(f"/users/email/{user_1['email']}")
    assert delete_user_1.status_code == 200

    # Ensure User 1 cannot be retrieved
    get_deleted_user_1 = client.get(f"/users/email/{user_1['email']}")
    assert get_deleted_user_1.status_code == 404

    # Delete User 2
    delete_user_2 = client.delete(f"/users/email/{user_2['email']}")
    assert delete_user_2.status_code == 200

    # Ensure User 2 cannot be retrieved
    get_deleted_user_2 = client.get(f"/users/email/{user_2['email']}")
    assert get_deleted_user_2.status_code == 404

def test_follow_unfollow_non_existent_users_and_delete():
    user_1 = {
        "email": "user1test@example.com",
        "is_active": True,
        "is_admin": False,
        "full_name": "User One",
        "password": "password123"
    }
    response_1 = client.post("/users/", json=user_1)
    assert response_1.status_code == 201
    user_1_data = response_1.json()
    user_1_id = user_1_data["id"]

    # Override the dependency
    app.dependency_overrides[get_current_user] = mock_get_current_user(user_1_id)

    # Try to follow a non-existent user
    non_existent_user_id = 9999  # Arbitrary non-existent user ID
    follow_response = client.post(f"/users/follow/{non_existent_user_id}", headers={"Authorization": "Bearer mock-token"})
    assert follow_response.status_code == 404  # Expect 404 Not Found

    # Try to unfollow a non-existent user
    unfollow_response = client.post(f"/users/unfollow/{non_existent_user_id}")
    assert unfollow_response.status_code == 500  # Expect 500 Not Found

    # Try to get followers of a non-existent user
    followers_response = client.get(f"/users/followers/{non_existent_user_id}")
    assert followers_response.status_code == 404  # Expect 404 Not Found

    # Try to get followed users of a non-existent user
    followed_response = client.get(f"/users/followed/{non_existent_user_id}")
    assert followed_response.status_code == 404  # Expect 404 Not Found

    # Delete User 1
    delete_user_1 = client.delete(f"/users/email/{user_1['email']}")
    assert delete_user_1.status_code == 200

    # Ensure User 1 cannot be retrieved
    get_deleted_user_1 = client.get(f"/users/email/{user_1['email']}")
    assert get_deleted_user_1.status_code == 404


def test_create_user_add_movie_and_manage_list():
    app.dependency_overrides[is_admin_user] = mock_is_admin_user
    # Create a premium user
    premium_user = {
        "email": "premiumuser@example.com",
        "is_active": True,
        "is_premium": True,
        "full_name": "Premium User",
        "password": "password123"
    }
    client.post("/users/", json=premium_user)

    # Create a movie
    new_movie = {
        "title": "The Lost City",
        "description": "A renowned archaeologist stumbles upon a hidden city filled with secrets, leading to a thrilling adventure across uncharted lands.",
        "director": "Sarah Connors",
        "country": "United States",
        "release_date": "2024-10-26",
        "rating": 4.2,
        "rating_count": 12500,
        "likes": 5200,
        "genres": ["Adventure", "Thriller"],
        "cast_members": ["John Doe", "Jane Smith", "Mike Johnson"],
        "image": [],
        "trailer": ""
    }
    movie_response = client.post("/movies/", json=new_movie)
    assert movie_response.status_code == 200

    # Create a list for the user
    list_type_data = {"name": "Watch Later"}
    response = client.post(f"/list-type/{premium_user['email']}/{list_type_data['name']}")
    assert response.status_code == 201
    assert response.json()["name"] == list_type_data["name"]

    # Add the movie to the list
    movie_data = movie_response.json()
    response2 = client.post(f"/list-type/add-movie/{premium_user['email']}/{list_type_data['name']}/{movie_data['id']}")
    assert response2.status_code == 200
    assert response2.json()["movie_id"] == movie_data['id']

    # Get the list by its name and check the movie
    response3 = client.get(f"/list-type/movies/{premium_user['email']}/{list_type_data['name']}")
    assert response3.status_code == 200
    assert response3.json() == ["The Lost City"]  # Movie should be in the list

    # Get the user's list with movies
    response4 = client.get(f"/list-type/get-lists-with-movies/{premium_user['email']}")
    assert response4.status_code == 200
    lists_with_movies = response4.json()
    assert len(lists_with_movies) == 1
    assert lists_with_movies[0]["list_name"] == "Watch Later"
    assert len(lists_with_movies[0]["movies"]) == 1
    assert lists_with_movies[0]["movies"][0]["title"] == "The Lost City"

    # Remove the movie from the list
    response5 = client.delete(f"/list-type/remove-movie/{premium_user['email']}/{list_type_data['name']}/{movie_data['id']}")
    assert response5.status_code == 200
    assert response5.json() == {"detail": f"Movie ID {movie_data['id']} removed from list '{list_type_data['name']}'."}

    # Delete the list
    response6 = client.delete(f"/list-type/{premium_user['email']}/{list_type_data['name']}")
    assert response6.status_code == 200
    assert response6.json() == {"detail": f"List '{list_type_data['name']}' deleted successfully."}

    # Delete the user
    response7 = client.delete(f"/users/email/{premium_user['email']}")
    assert response7.status_code == 200

    # Delete the movie
    response8 = client.delete(f"/movies/title/{new_movie['title']}")
    assert response8.status_code == 200

def test_non_premium_user_try_create_list_and_movie_operations():
    app.dependency_overrides[is_admin_user] = mock_is_admin_user
    # Create a non-premium user
    non_premium_user = {
        "email": "nonpremiumuser@example.com",
        "is_active": True,
        "is_premium": False,
        "full_name": "Non-Premium User",
        "password": "password123"
    }
    client.post("/users/", json=non_premium_user)

    # Create a movie
    new_movie = {
        "title": "The Lost City",
        "description": "A renowned archaeologist stumbles upon a hidden city filled with secrets, leading to a thrilling adventure across uncharted lands.",
        "director": "Sarah Connors",
        "country": "United States",
        "release_date": "2024-10-26",
        "rating": 4.2,
        "rating_count": 12500,
        "likes": 5200,
        "genres": ["Adventure", "Thriller"],
        "cast_members": ["John Doe", "Jane Smith", "Mike Johnson"],
        "image": [],
        "trailer": ""
    }
    movie_response = client.post("/movies/", json=new_movie)
    assert movie_response.status_code == 200

    # Non-premium user tries to create a list
    list_type_data = {"name": "Watch Later"}
    response = client.post(f"/list-type/{non_premium_user['email']}/{list_type_data['name']}")
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found or unable to create list"

    # Step 4: Delete the non-premium user
    response2 = client.delete(f"/users/email/{non_premium_user['email']}")
    assert response2.status_code == 200

    # Create a premium user
    premium_user = {
        "email": "premiumuser@example.com",
        "is_active": True,
        "is_premium": True,
        "full_name": "Premium User",
        "password": "password123"
    }
    client.post("/users/", json=premium_user)

    # Create a list with the premium user
    list_type_data = {"name": "Watch Later"}
    response3 = client.post(f"/list-type/{premium_user['email']}/{list_type_data['name']}")
    assert response3.status_code == 201
    assert response3.json()["name"] == list_type_data["name"]

    # Try to add a movie that doesn't exist to the list
    response4 = client.post(f"/list-type/add-movie/{premium_user['email']}/{list_type_data['name']}/9999")
    assert response4.status_code == 404
    assert response4.json() == {"detail": "Movie not found"}

    # Try to add the movie to a non-existing list
    response5 = client.post(f"/list-type/add-movie/{premium_user['email']}/NonExistentList/{movie_response.json()['id']}")
    assert response5.status_code == 404
    assert response5.json() == {"detail": "List not found"}

    # Delete the list
    response6 = client.delete(f"/list-type/{premium_user['email']}/{list_type_data['name']}")
    assert response6.status_code == 200
    assert response6.json() == {"detail": f"List '{list_type_data['name']}' deleted successfully."}

    # Delete the movie
    response7 = client.delete(f"/movies/title/{new_movie['title']}")
    assert response7.status_code == 200

    # Delete the premium user
    response8 = client.delete(f"/users/email/{premium_user['email']}")
    assert response8.status_code == 200
