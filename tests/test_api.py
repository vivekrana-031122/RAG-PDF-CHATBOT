import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_get_invalid_session():
    response = client.get("/session/invalid_id")
    assert response.status_code == 404

def test_ask_invalid_session():
    response = client.post("/ask/invalid_id", json={"question": "What is life?"})
    assert response.status_code == 404
