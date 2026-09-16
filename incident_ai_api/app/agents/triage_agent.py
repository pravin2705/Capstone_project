from typing import Any
 
from app.agents.input_validator import (
    IncidentInputValidator,
)
from app.agents.recommender import AgentRecommender
from app.agents.router import AgentRouter
from app.agents.safety import SafetyChecker
from app.services.safe_tool_runner import SafeToolRunner
from app.workflow.termination import WorkflowTerminator
 
 
class TriageAgent:
    """
    Stateful maintenance triage agent.
 
    The same case object is passed through the
    complete workflow.
    """
 
    def __init__(
        self,
        rag_tool: Any,
        maintenance_tool: Any,
        telemetry_tool: Any,
        inventory_tool: Any,
    ):
        self.rag_tool = rag_tool
        self.maintenance_tool = maintenance_tool
        self.telemetry_tool = telemetry_tool
        self.inventory_tool = inventory_tool
 
        self.validator = IncidentInputValidator()
        self.router = AgentRouter()
        self.recommender = AgentRecommender()
        self.safety_checker = SafetyChecker()
        self.terminator = WorkflowTerminator()
        self.tool_runner = SafeToolRunner()
 
    def run(self, case):
 
        # ------------------------------------------------
        # 1. Validate input
        # ------------------------------------------------
 
        validation = self.validator.validate(case)
 
        if not validation["valid"]:
 
            case.errors.append(
                validation["message"]
            )
 
            return {
                "status": "INCOMPLETE",
                "case": case,
                "validation": validation,
            }
 
        # ------------------------------------------------
        # 2. Select tools
        # ------------------------------------------------
 
        selected_tools = self.router.select_tools(
            case.alarm
        )
 
        case.selected_tools = selected_tools
 
        # ------------------------------------------------
        # 3. RAG Knowledge
        # ------------------------------------------------
 
        rag_results = []
 
        if "rag" in selected_tools:
 
            rag_results = self.tool_runner.run(
                case,
                "rag",
                self.rag_tool.search_knowledge,
                query=case.alarm,
                machine_model=case.machine_model,
                manual_version=case.manual_version,
            )
 
            if rag_results is None:
                rag_results = []
 
        case.rag_evidence = rag_results
 
        # ------------------------------------------------
        # 4. Maintenance History
        # ------------------------------------------------
 
        maintenance_history = []
 
        if "maintenance" in selected_tools:
 
            maintenance_history = self.tool_runner.run(
                case,
                "maintenance",
                self.maintenance_tool.get_history,
                case.asset_id,
            )
 
            if maintenance_history is None:
                maintenance_history = []
 
        case.maintenance_history = maintenance_history
 
        # ------------------------------------------------
        # 5. Telemetry
        # ------------------------------------------------
 
        telemetry = {}
 
        if "telemetry" in selected_tools:
 
            telemetry_result = self.tool_runner.run(
                case,
                "telemetry",
                self.telemetry_tool.get_telemetry,
                case.asset_id,
            )
 
            if telemetry_result is not None:
                telemetry = telemetry_result
 
        case.telemetry = telemetry
 
        # ------------------------------------------------
        # 6. Spare Inventory
        # ------------------------------------------------
 
        spare_inventory = []
 
        if "inventory" in selected_tools:
 
            spare_inventory = self.tool_runner.run(
                case,
                "inventory",
                self.inventory_tool.get_inventory,
            )
 
            if spare_inventory is None:
                spare_inventory = []
 
        case.spare_inventory = spare_inventory
 
        # ------------------------------------------------
        # 7. Recommendation
        # ------------------------------------------------
 
        recommendation = self.recommender.recommend(
            alarm=case.alarm,
            telemetry=telemetry,
            maintenance_history=maintenance_history,
            spare_inventory=spare_inventory,
            rag_evidence=rag_results,
        )
 
        case.recommended_action = recommendation
 
        if "recommendation" not in case.completed_steps:
            case.completed_steps.append(
                "recommendation"
            )
 
        # ------------------------------------------------
        # 8. Safety Check
        # ------------------------------------------------
 
        safety_result = self.safety_checker.check(
            telemetry=telemetry,
            severity=getattr(
                case,
                "severity",
                "HIGH",
            ),
        )
 
        case.safety_status = safety_result["status"]
 
        if "safety" not in case.completed_steps:
            case.completed_steps.append("safety")
 
        # ------------------------------------------------
        # 9. Termination
        # ------------------------------------------------
 
        terminated = self.terminator.should_terminate(
            case
        )
 
        if terminated:
 
            return {
                "status": "READY_FOR_HITL",
                "case": case,
                "termination_reason": (
                    self.terminator.termination_reason(
                        case
                    )
                ),
            }
 
        return {
            "status": "INVESTIGATION_INCOMPLETE",
            "case": case,
            "termination_reason": (
                self.terminator.termination_reason(
                    case
                )
            ),
        }
 