import pytest
 
from app.providers.mock_provider import MockLLMProvider
 
 
@pytest.mark.parametrize(
    "incident, expected_type, expected_severity",
    [
        (
            {
                "asset_id": "PUMP-101",
                "alarm": "High temperature",
                "description": "Pump temperature is above normal",
            },
            "OVERHEATING",
            "HIGH",
        ),
        (
            {
                "asset_id": "MOTOR-201",
                "alarm": "Excessive vibration",
                "description": "Motor vibration is increasing",
            },
            "VIBRATION",
            "MEDIUM",
        ),
        (
            {
                "asset_id": "COMP-301",
                "alarm": "High pressure",
                "description": "Compressor pressure is above normal",
            },
            "HIGH_PRESSURE",
            "HIGH",
        ),
        (
            {
                "asset_id": "TANK-401",
                "alarm": "Oil leak detected",
                "description": "Oil leakage observed",
            },
            "LEAK",
            "HIGH",
        ),
    ],
)
def test_incident_classification(
    incident,
    expected_type,
    expected_severity,
):
    provider = MockLLMProvider()
 
    result = provider.analyze_incident(incident)
 
    assert result.incident_type.value == expected_type
    assert result.severity.value == expected_severity
    assert result.facts["asset_id"] == incident["asset_id"]
 