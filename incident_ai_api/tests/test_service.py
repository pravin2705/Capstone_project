from app.providers.mock_provider import MockLLMProvider
from app.schemas.incident import IncidentRequest
from app.services.incident_service import IncidentService
 
 
def test_incident_service():
    provider = MockLLMProvider()
    service = IncidentService(provider)
 
    incident = IncidentRequest(
        asset_id="PUMP-101",
        alarm="High temperature",
        description="Pump is making unusual noise",
        temperature=98,
        pressure=7.2,
        vibration=8.5
    )
 
    result = service.process_incident(incident)
 
    assert result.incident_type.value == "OVERHEATING"
    assert result.severity.value == "HIGH"
    assert result.facts["asset_id"] == "PUMP-101"
    assert result.facts["alarm"] == "High temperature"