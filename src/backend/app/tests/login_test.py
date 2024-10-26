from fastapi.testclient import TestClient
from app.main import app  # Asegúrate de que la importación sea correcta
import pytest

client = TestClient(app)

# Primero, crea un usuario para poder iniciar sesión
@pytest.fixture
def create_user():
    new_user = {
        "email": "testlogin@example.com",
        "password": "password123",
        "is_active": True,
        "is_admin": False,
        "full_name": "Test Login"
    }
    
    # Crear un nuevo usuario
    response = client.post("/users/", json=new_user)
    yield new_user
    # Eliminar el usuario después de la prueba
    user_data = response.json()
    client.delete(f"/users/{user_data['id']}")

def test_login_for_access_token(create_user):
    # Intenta iniciar sesión
    response = client.post(
        "/login/",
        data={
            "username": create_user["email"],
            "password": create_user["password"]
        }
    )
    
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"

def test_login_failed_with_incorrect_password(create_user):
    # Intenta iniciar sesión con una contraseña incorrecta
    response = client.post(
        "/login/",
        data={
            "username": create_user["email"],
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_read_users_me(create_user):
    # Inicia sesión para obtener el token
    login_response = client.post(
        "/login/",
        data={
            "username": create_user["email"],
            "password": create_user["password"]
        }
    )
    access_token = login_response.json()["access_token"]
    
    # Usa el token para obtener el usuario actual
    response = client.get(
        "/login/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["email"] == create_user["email"]
    assert response_data["full_name"] == create_user["full_name"]

def test_test_token(create_user):
    # Inicia sesión para obtener el token
    login_response = client.post(
        "/login/",
        data={
            "username": create_user["email"],
            "password": create_user["password"]
        }
    )
    access_token = login_response.json()["access_token"]
    
    # Prueba el token
    response = client.post(
        "/login/test-token",
        json={"token": access_token}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "Token is valid"
    assert response.json()["user"]["email"] == create_user["email"]
