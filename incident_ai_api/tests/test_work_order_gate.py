from app.schemas.case_state import CaseState
from app.workflow.work_order_gate import WorkOrderGate
 
 
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
        hitl_status="PENDING",
    )
 
 
def test_work_order_blocked_without_engineer_approval():
 
    case = create_case()
 
    gate = WorkOrderGate()
 
    result = gate.create_if_approved(case)
 
    assert result["status"] == "BLOCKED"
 
    assert result["work_order"] is None
 
    assert "engineer approval" in (
        result["reason"].lower()
    )
 
 
def test_work_order_created_after_approval():
 
    case = create_case()
 
    case.hitl_status = "APPROVED"
 
    gate = WorkOrderGate()
 
    result = gate.create_if_approved(case)
 
    assert result["status"] == "CREATED"
 
    assert result["work_order"] is not None
 
    assert (
        result["work_order"]["work_order_id"]
        == "WO-001"
    )
 
    assert case.work_order is not None
 
    assert "work_order_created" in (
        case.completed_steps
    )
 
 
def test_work_order_blocked_when_safety_fails():
 
    case = create_case()
 
    case.hitl_status = "APPROVED"
    case.safety_status = "BLOCKED"
 
    gate = WorkOrderGate()
 
    result = gate.create_if_approved(case)
 
    assert result["status"] == "BLOCKED"
 
    assert result["work_order"] is None
 
    assert "safety" in (
        result["reason"].lower()
    )
 
 
def test_work_order_blocked_without_recommendation():
 
    case = create_case()
 
    case.hitl_status = "APPROVED"
    case.recommended_action = None
 
    gate = WorkOrderGate()
 
    result = gate.create_if_approved(case)
 
    assert result["status"] == "BLOCKED"
 
    assert result["work_order"] is None