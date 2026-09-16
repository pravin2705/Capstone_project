from fastapi.testclient import TestClient
 
from app.main import app
 
 
client = TestClient(app)
 
 
def test_create_incident_success():
    response = client.post(
        "/incidents",
        json={
            "asset_id": "PUMP-101",
            "alarm": "High temperature",
            "description": "Pump is making unusual noise",
            "temperature": 98,
            "pressure": 7.2,
            "vibration": 8.5
        }
    )
 
    assert response.status_code == 200
 
    data = response.json()
 
    assert data["incident_type"] == "OVERHEATING"
    assert data["severity"] == "HIGH"
    assert data["facts"]["asset_id"] == "PUMP-101"
    assert "summary" in data
 
 
def test_create_incident_invalid_request():
    response = client.post(
        "/incidents",
        json={
            "asset_id": "",
            "alarm": "",
            "description": ""
        }
    )
 
    assert response.status_code == 422