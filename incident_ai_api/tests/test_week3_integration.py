from app.agents.triage_agent import TriageAgent
from app.schemas.case_state import CaseState
from app.workflow.hitl import EngineerHITL
from app.workflow.work_order_gate import WorkOrderGate
 
 
# ============================================================
# Mock Tools
# ============================================================
 
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
                "issue": "Previous overheating",
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
 
 
# ============================================================
# Helper
# ============================================================
 
def create_agent():
 
    return TriageAgent(
        rag_tool=MockRAGTool(),
        maintenance_tool=MockMaintenanceTool(),
        telemetry_tool=MockTelemetryTool(),
        inventory_tool=MockInventoryTool(),
    )
 
 
def create_case():
 
    return CaseState(
        case_id="CASE-W3-001",
        asset_id="PUMP-101",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
    )
 
 
# ============================================================
# Test 1
# Normal flow
# ============================================================
 
def test_week3_normal_flow():
 
    case = create_case()
 
    agent = create_agent()
 
    result = agent.run(case)
 
    # Agent investigation completed
    assert result["status"] == "READY_FOR_HITL"
 
    # State preserved
    assert case.rag_evidence
    assert case.maintenance_history
    assert case.telemetry
    assert case.spare_inventory
 
    # Recommendation generated
    assert case.recommended_action
 
    # Safety passed
    assert case.safety_status == "PASSED"
 
    # --------------------------------------------------------
    # Engineer approval
    # --------------------------------------------------------
 
    hitl = EngineerHITL()
 
    hitl.approve(case)
 
    assert case.hitl_status == "APPROVED"
 
    # --------------------------------------------------------
    # Work order
    # --------------------------------------------------------
 
    gate = WorkOrderGate()
 
    result = gate.create_if_approved(case)
 
    assert result["status"] == "CREATED"
 
    assert case.work_order is not None
 
 
# ============================================================
# Test 2
# Engineer rejects recommendation
# ============================================================
 
def test_week3_engineer_rejection():
 
    case = create_case()
 
    agent = create_agent()
 
    result = agent.run(case)
 
    assert result["status"] == "READY_FOR_HITL"
 
    # Engineer rejects
    hitl = EngineerHITL()
 
    hitl.reject(case)
 
    assert case.hitl_status == "REJECTED"
 
    # Work order must NOT be created
    gate = WorkOrderGate()
 
    result = gate.create_if_approved(case)
 
    assert result["status"] == "BLOCKED"
 
    assert result["work_order"] is None
 
    assert case.work_order is None
 
 
# ============================================================
# Test 3
# Incomplete input
# ============================================================
 
def test_week3_incomplete_input():
 
    case = CaseState(
        case_id="CASE-W3-003",
        asset_id="",
        machine_model="PX-500",
        alarm="High Temperature Alarm",
    )
 
    agent = create_agent()
 
    result = agent.run(case)
 
    # Workflow must stop safely
    assert result["status"] == "INCOMPLETE"
 
    # No work order
    assert case.work_order is None
 
    # Error should be recorded
    assert case.errors
 
 
# ============================================================
# Test 4
# Safety blocks work order
# ============================================================
 
def test_week3_safety_blocks_work_order():
 
    case = create_case()
 
    agent = create_agent()
 
    result = agent.run(case)
 
    assert result["status"] == "READY_FOR_HITL"
 
    # Engineer approves
    hitl = EngineerHITL()
 
    hitl.approve(case)
 
    # Force safety failure
    case.safety_status = "BLOCKED"
 
    gate = WorkOrderGate()
 
    result = gate.create_if_approved(case)
 
    assert result["status"] == "BLOCKED"
 
    assert result["work_order"] is None
 
    assert case.work_order is None