from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_species():
    response = client.get("/species", params={"n": 3, "page": 1})
    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()["results"]) == 3

def test_get_species():
    response = client.get("/species/1")
    assert response.status_code == 200
    assert response.json() is not None