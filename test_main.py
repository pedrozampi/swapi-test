from fastapi.testclient import TestClient
from main import app
import random
import string

client = TestClient(app)

token = None
username = None

def generate_username():
    return f"test_user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"

def test_register():
    global username
    username = generate_username()
    password = "test123"
    response = client.post("/register", json={"username": username, "password": password})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_token():
    global token
    password = "test123"
    response = client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

def test_add_favorite():
    response = client.post("/favorites/films", params={"item_id": "1"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Favorite added successfully"}

def test_get_favorite():
    client.post("/favorites/films", params={"item_id": "1"}, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/favorites/films", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    favorite = response.json()
    assert favorite is not None
    assert favorite["type"] == "films"
    assert favorite["item_id"] == "1"

def test_get_favorites():
    client.post("/favorites/films", params={"item_id": "1"}, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/favorites", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    favorites = response.json()
    assert isinstance(favorites, list)
    assert len(favorites) > 0

def test_delete_favorite():
    response = client.delete("/favorites/films", params={"item_id": "1"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Favorite deleted successfully"}

def test_delete_user():
    response = client.delete("/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

