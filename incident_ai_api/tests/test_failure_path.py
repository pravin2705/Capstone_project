from app.agents.triage_agent import TriageAgent
from app.schemas.case_state import CaseState
 
 
class MockRAGTool:
 
    def search_knowledge(
        self,
        query,
        machine_model,
        manual_version=None,
    ):
        return [
            {
                "text": "Inspect cooling system.",
                "metadata": {
                    "machine_model": machine_model,
                    "manual_version": manual_version,
                },
                "score": 0.95,
            }
        ]
 
 
class MockMaintenanceTool:
 
    def get_history(self, asset_id):
 
        return [
            {
                "asset_id": asset_id,
                "issue": "Previous overheating",
            }
        ]
 
 
class UnavailableTelemetryTool:
 
    def get_telemetry(self, asset_id):
 
        raise RuntimeError(
            "Telemetry service unavailable"
        )
 
 
class MockInventoryTool:
 
    def get_inventory(self):
 
        return [
            {
                "part_name": "Cooling Fan",
                "quantity": 2,
                "status": "AVAILABLE",
            }
        ]
 
 
def test_unavailable_telemetry_is_handled():
 
    case = CaseState(
        case_id="CASE-FAIL-001",
        asset_id="PUMP-101",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
    )
 
    agent = TriageAgent(
        rag_tool=MockRAGTool(),
        maintenance_tool=MockMaintenanceTool(),
        telemetry_tool=UnavailableTelemetryTool(),
        inventory_tool=MockInventoryTool(),
    )
 
    # The workflow should NOT raise an exception.
    result = agent.run(case)
 
    # Workflow should return a controlled result.
    assert result is not None
 
    # Telemetry should not be marked as successfully completed.
    assert "telemetry" not in case.completed_steps
 
    # Failure should be stored in case state.
    assert len(case.errors) > 0
 
    assert any(
        "telemetry" in error.lower()
        for error in case.errors
    )