from app.schemas.case_state import CaseState
from app.workflow.termination import WorkflowTerminator
 
 
def test_workflow_can_terminate():
 
    case = CaseState(
        case_id="CASE-001",
        asset_id="PUMP-101",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
    )
 
    case.completed_steps = [
        "rag",
        "maintenance",
        "telemetry",
        "recommendation",
        "safety",
    ]
 
    terminator = WorkflowTerminator()
 
    assert terminator.should_terminate(case) is True
 
 
def test_workflow_cannot_terminate():
 
    case = CaseState(
        case_id="CASE-002",
        asset_id="PUMP-101",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
    )
 
    case.completed_steps = [
        "rag",
        "maintenance",
        "telemetry",
    ]
 
    terminator = WorkflowTerminator()
 
    assert terminator.should_terminate(case) is False
 
 
def test_termination_reason():
 
    case = CaseState(
        case_id="CASE-003",
        asset_id="PUMP-101",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
    )
 
    case.completed_steps = [
        "rag",
        "maintenance",
        "telemetry",
        "recommendation",
        "safety",
    ]
 
    terminator = WorkflowTerminator()
 
    reason = terminator.termination_reason(case)
 
    assert "Engineer approval" in reason