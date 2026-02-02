from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_people():
    response = client.get("/people", params={"n": 3, "page": 1})
    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()["results"]) == 3

def test_get_person():
    response = client.get("/people/1")
    assert response.status_code == 200
    assert response.json() is not None