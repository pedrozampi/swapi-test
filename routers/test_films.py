from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_films():
    response = client.get("/films", params={"n": 3, "page": 1})
    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()["results"]) == 3

def test_get_film():
    response = client.get("/films/1")
    assert response.status_code == 200
    assert response.json() is not None