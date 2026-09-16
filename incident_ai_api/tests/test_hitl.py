import pytest
 
from app.schemas.case_state import CaseState
from app.workflow.hitl import EngineerHITL
 
 
def create_case():
    return CaseState(
        case_id="CASE-001",
        asset_id="PUMP-101",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
        recommended_action=(
            "Inspect cooling system."
        ),
        safety_status="PASSED",
    )
 
 
def test_approval_request():
 
    case = create_case()
 
    hitl = EngineerHITL()
 
    request = hitl.request_approval(case)
 
    assert request["case_id"] == "CASE-001"
    assert request["asset_id"] == "PUMP-101"
    assert request["status"] == "PENDING"
 
 
def test_engineer_approval():
 
    case = create_case()
 
    hitl = EngineerHITL()
 
    updated_case = hitl.approve(case)
 
    assert updated_case.hitl_status == "APPROVED"
    assert "hitl_approved" in (
        updated_case.completed_steps
    )
 
 
def test_engineer_rejection():
 
    case = create_case()
 
    hitl = EngineerHITL()
 
    updated_case = hitl.reject(case)
 
    assert updated_case.hitl_status == "REJECTED"
    assert "hitl_rejected" in (
        updated_case.completed_steps
    )
 
 
def test_approval_blocked_without_safety():
 
    case = create_case()
 
    case.safety_status = "BLOCKED"
 
    hitl = EngineerHITL()
 
    with pytest.raises(ValueError):
 
        hitl.approve(case)