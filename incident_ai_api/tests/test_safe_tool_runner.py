from app.schemas.case_state import CaseState
from app.services.safe_tool_runner import SafeToolRunner
from app.services.tool_executor import ToolExecutor
 
 
def create_case():
    return CaseState(
        case_id="CASE-001",
        asset_id="PUMP-101",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
    )
 
 
def test_successful_tool():
 
    case = create_case()
 
    runner = SafeToolRunner(
        ToolExecutor(max_retries=1)
    )
 
    def successful_tool():
        return {
            "temperature": 95.0
        }
 
    result = runner.run(
        case,
        "telemetry",
        successful_tool,
    )
 
    assert result["temperature"] == 95.0
    assert "telemetry" in case.completed_steps
    assert case.errors == []
 
 
def test_unavailable_tool():
 
    case = create_case()
 
    runner = SafeToolRunner(
        ToolExecutor(max_retries=1)
    )
 
    def unavailable_tool():
        raise RuntimeError(
            "Telemetry service unavailable"
        )
 
    result = runner.run(
        case,
        "telemetry",
        unavailable_tool,
    )
 
    assert result is None
 
    assert len(case.errors) == 1
 
    assert "telemetry" in case.errors[0]
 
 
def test_tool_failure_does_not_crash_workflow():
 
    case = create_case()
 
    runner = SafeToolRunner(
        ToolExecutor(max_retries=1)
    )
 
    def failing_tool():
        raise RuntimeError("Service unavailable")
 
    # The workflow should continue without
    # raising the original exception.
    result = runner.run(
        case,
        "maintenance",
        failing_tool,
    )
 
    assert result is None
 
    assert case.errors