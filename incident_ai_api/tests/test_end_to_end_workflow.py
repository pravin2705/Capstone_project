from app.agents.triage_agent import TriageAgent
from app.schemas.case_state import CaseState
from app.workflow.hitl import EngineerHITL
from app.workflow.work_order_gate import WorkOrderGate
 
 
class MockRAGTool:
 
    def search_knowledge(
        self,
        query,
        machine_model,
        manual_version=None,
    ):
        return [
            {
                "text": (
                    "For high temperature alarms, "
                    "inspect the cooling system."
                ),
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
                "issue": "Previous high temperature issue",
                "action": "Cooling system inspected",
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
 
 
def create_agent():
 
    return TriageAgent(
        rag_tool=MockRAGTool(),
        maintenance_tool=MockMaintenanceTool(),
        telemetry_tool=MockTelemetryTool(),
        inventory_tool=MockInventoryTool(),
    )
 
 
def test_complete_end_to_end_workflow():
 
    # --------------------------------------------------
    # 1. Create case
    # --------------------------------------------------
 
    case = CaseState(
        case_id="CASE-E2E-001",
        asset_id="PUMP-101",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
    )
 
    # --------------------------------------------------
    # 2. Run agent investigation
    # --------------------------------------------------
 
    agent = create_agent()
 
    result = agent.run(case)
 
    assert result["status"] == "READY_FOR_HITL"
 
    # --------------------------------------------------
    # 3. Verify state was preserved
    # --------------------------------------------------
 
    assert case.rag_evidence
 
    assert case.maintenance_history
 
    assert case.telemetry
 
    assert case.spare_inventory
 
    assert case.recommended_action
 
    assert case.safety_status == "PASSED"
 
    # --------------------------------------------------
    # 4. Verify termination
    # --------------------------------------------------
 
    assert "rag" in case.completed_steps
 
    assert "maintenance" in case.completed_steps
 
    assert "telemetry" in case.completed_steps
 
    assert "inventory" in case.completed_steps
 
    assert "recommendation" in case.completed_steps
 
    assert "safety" in case.completed_steps
 
    # --------------------------------------------------
    # 5. Engineer HITL
    # --------------------------------------------------
 
    hitl = EngineerHITL()
 
    approval_request = hitl.request_approval(case)
 
    assert approval_request["status"] == "PENDING"
 
    approved_case = hitl.approve(case)
 
    assert approved_case.hitl_status == "APPROVED"
 
    assert "hitl_approved" in (
        approved_case.completed_steps
    )
 
    # --------------------------------------------------
    # 6. Work-order gate
    # --------------------------------------------------
 
    gate = WorkOrderGate()
 
    work_order_result = gate.create_if_approved(
        approved_case
    )
 
    # --------------------------------------------------
    # 7. Verify work order
    # --------------------------------------------------
 
    assert work_order_result["status"] == "CREATED"
 
    assert work_order_result["work_order"] is not None
 
    work_order = work_order_result["work_order"]
 
    assert work_order["case_id"] == "CASE-E2E-001"
 
    assert work_order["asset_id"] == "PUMP-101"
 
    assert work_order["status"] == "CREATED"
 
    assert approved_case.work_order is not None
 
    assert "work_order_created" in (
        approved_case.completed_steps
    )