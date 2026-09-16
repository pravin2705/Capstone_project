from fastapi.testclient import TestClient
 
from app.main import app
 
 
client = TestClient(app)
 
 
def test_triage_api_success():
    payload = {
        "case_id": "CASE-001",
        "asset_id": "PUMP-101",
        "machine_model": "PX-500",
        "manual_version": "v1.0",
        "alarm": "High Temperature Alarm",
    }
 
    response = client.post(
        "/triage",
        json=payload,
    )
 
    assert response.status_code == 200
 
    data = response.json()
 
    assert data["case_id"] == "CASE-001"
    assert data["status"] == "READY_FOR_HITL"
    assert "recommended_action" in data
    assert "safety_status" in data
    assert "hitl_status" in data