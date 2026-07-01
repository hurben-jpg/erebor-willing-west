from fastapi.testclient import TestClient
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
import shutil

# Clean up previous test DB if exists
if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "I am Erebor. I am the building."}

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Erebor"
    assert "sensors" in data

def test_chat_flow():
    # 1. First interaction
    response = client.post("/chat", json={"message": "Hello, who are you?"})
    assert response.status_code == 200
    reply = response.json()["response"]
    print(f"Erebor says: {reply}")
    assert "Erebor" in reply or "building" in reply.lower()

    # 2. Second interaction (testing memory implicitly via no crash)
    response = client.post("/chat", json={"message": "Is it cold outside?"})
    assert response.status_code == 200
    reply = response.json()["response"]
    print(f"Erebor says: {reply}")
    assert "Temperature" in reply or "sensors" in reply

if __name__ == "__main__":
    test_root()
    test_status()
    test_chat_flow()
    print("All tests passed!")
