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
                "issue": "High temperature",
            }
        ]
 
 
class MockTelemetryTool:
 
    def get_telemetry(self, asset_id):
 
        return {
            "temperature": 95.0,
            "vibration": 2.0,
            "pressure": 4.0,
        }
 
 
class MockInventoryTool:
 
    def get_inventory(self):
 
        return [
            {
                "part_name": "Cooling Fan",
                "quantity": 2,
                "status": "AVAILABLE",
            }
        ]
 
 
def test_triage_agent():
 
    case = CaseState(
        case_id="CASE-001",
        asset_id="PUMP-101",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
    )
 
    agent = TriageAgent(
        rag_tool=MockRAGTool(),
        maintenance_tool=MockMaintenanceTool(),
        telemetry_tool=MockTelemetryTool(),
        inventory_tool=MockInventoryTool(),
    )
 
    result = agent.run(case)
 
    assert result["status"] == "READY_FOR_HITL"
 
    assert case.recommended_action is not None
 
    assert case.safety_status == "PASSED"
 
    assert "rag" in case.completed_steps
 
    assert "maintenance" in case.completed_steps
 
    assert "telemetry" in case.completed_steps
 
    assert "inventory" in case.completed_steps
 
    assert "recommendation" in case.completed_steps
 
    assert "safety" in case.completed_steps