from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home():
    response = client.get("/")  # Use TestClient's get method
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI app. Use /ask to submit your query."}
