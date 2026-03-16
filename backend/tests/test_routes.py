import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_upload_rejects_non_csv():
    response = client.post("/api/upload", files={"file": ("test.txt", b"data", "text/plain")})
    assert response.status_code == 400

def test_upload_valid_csv():
    csv_content = "name,value\nA,1\nB,2\nC,3"
    response = client.post("/api/upload", files={"file": ("test.csv", csv_content, "text/csv")})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["rows"] == 3
    assert data["columns"] == 2
