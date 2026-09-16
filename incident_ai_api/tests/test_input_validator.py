from app.agents.input_validator import (
    IncidentInputValidator,
)
from app.schemas.case_state import CaseState
 
 
def test_complete_input():
 
    case = CaseState(
        case_id="CASE-001",
        asset_id="PUMP-101",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
    )
 
    validator = IncidentInputValidator()
 
    result = validator.validate(case)
 
    assert result["valid"] is True
    assert result["status"] == "VALID"
    assert result["missing_fields"] == []
 
 
def test_missing_machine_model():
 
    case = CaseState(
        case_id="CASE-002",
        asset_id="PUMP-101",
        machine_model="",
        alarm="High Temperature Alarm",
    )
 
    validator = IncidentInputValidator()
 
    result = validator.validate(case)
 
    assert result["valid"] is False
    assert result["status"] == "INCOMPLETE"
 
    assert "machine_model" in result["missing_fields"]
 
 
def test_missing_asset_and_alarm():
 
    case = CaseState(
        case_id="CASE-003",
        asset_id="",
        machine_model="PX-500",
        alarm="",
    )
 
    validator = IncidentInputValidator()
 
    result = validator.validate(case)
 
    assert result["valid"] is False
 
    assert "asset_id" in result["missing_fields"]
    assert "alarm" in result["missing_fields"]