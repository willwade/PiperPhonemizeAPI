from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_phonemize_endpoint():
    test_data = {
        "text": "hello",
        "language": "en-us"
    }
    response = client.post("/phonemize", json=test_data)
    assert response.status_code == 200
    assert "ipa" in response.json()
    assert "sampa" in response.json()
    assert "espeak_ascii" in response.json()

def test_phonemize_invalid_language():
    test_data = {
        "text": "hello",
        "language": "invalid-lang"
    }
    response = client.post("/phonemize", json=test_data)
    assert response.status_code == 500 