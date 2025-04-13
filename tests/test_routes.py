# tests/test_routes.py
import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    # Check that the index message contains a key phrase.
    # assert "Royal AI" in response.get_data(as_text=True)

def test_llm_endpoint(client):
    response = client.post("/llm", json={"prompt": "Hello Caelum!"})
    assert response.status_code == 200
    # Expect the default prompt to end with a check-in like "Is this helpful?" Uncomment the following
    # assert "Is this helpful" in response.get_data(as_text=True)

