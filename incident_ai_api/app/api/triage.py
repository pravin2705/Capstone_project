from fastapi import APIRouter, HTTPException
 
from app.schemas.triage import TriageRequest, TriageResponse
from app.schemas.case_state import CaseState
 
from app.tools.rag_tool import RAGKnowledgeTool
from app.tools.maintenance import get_maintenance_history
from app.tools.telemetry import get_telemetry
from app.tools.inventory import check_inventory
 
 
 
router = APIRouter()
 
 
# ---------------------------------------------------------
# Tool initialization
# ---------------------------------------------------------
 
rag_tool = RAGKnowledgeTool()
 
# These are FUNCTIONS, not classes.
maintenance_tool = get_maintenance_history
telemetry_tool = get_telemetry
inventory_tool = check_inventory
 
 
# ---------------------------------------------------------
# TRIAGE API
# ---------------------------------------------------------
 
@router.post(
    "/triage",
    response_model=TriageResponse,
)
async def run_triage(request: TriageRequest):
 
    try:
 
        # -------------------------------------------------
        # Create initial case state
        # -------------------------------------------------
 
        case = CaseState(
            case_id=request.case_id,
            asset_id=request.asset_id,
            machine_model=request.machine_model,
            manual_version=request.manual_version,
            alarm=request.alarm,
            selected_tools=[],
            completed_steps=[],
            errors=[],
            rag_evidence=[],
            maintenance_history=[],
            telemetry={},
            spare_inventory=[],
            inventory=[],
            recommended_action=None,
            safety_status="PENDING",
            hitl_status="PENDING",
            work_order=None,
        )
 
        # -------------------------------------------------
        # 1. RAG
        # -------------------------------------------------
 
        case.selected_tools.append("rag")
 
        try:
            case.rag_evidence = rag_tool.search(
                query=request.alarm,
                machine_model=request.machine_model,
                manual_version=request.manual_version,
            )
 
            case.completed_steps.append("rag")
 
        except Exception as exc:
            case.errors.append(
                f"rag tool failed: {str(exc)}"
            )
 
 
        # -------------------------------------------------
        # 2. Maintenance
        # -------------------------------------------------
 
        case.selected_tools.append("maintenance")
 
        try:
            # IMPORTANT:
            # get_maintenance_history is a function.
            # Do NOT use .get_history()
            case.maintenance_history = maintenance_tool(
                request.asset_id
            )
 
            case.completed_steps.append("maintenance")
 
        except Exception as exc:
            case.errors.append(
                f"maintenance tool failed: {str(exc)}"
            )
 
 
        # -------------------------------------------------
        # 3. Telemetry
        # -------------------------------------------------
 
        case.selected_tools.append("telemetry")
 
        try:
            case.telemetry = telemetry_tool(
                request.asset_id
            )
 
            case.completed_steps.append("telemetry")
 
        except Exception as exc:
            case.errors.append(
                f"telemetry tool failed: {str(exc)}"
            )
 
 
        # -------------------------------------------------
        # 4. Inventory
        # -------------------------------------------------
 
        case.selected_tools.append("inventory")
 
        try:
            case.inventory = inventory_tool(
                request.asset_id
            )
 
            case.spare_inventory = case.inventory
 
            case.completed_steps.append("inventory")
 
        except Exception as exc:
            case.errors.append(
                f"inventory tool failed: {str(exc)}"
            )
 
 
        # -------------------------------------------------
        # 5. Recommendation
        # -------------------------------------------------
 
        try:
 
            case.recommended_action = get_recommendation(
                alarm=request.alarm,
                telemetry=case.telemetry,
                rag_evidence=case.rag_evidence,
                maintenance_history=case.maintenance_history,
            )
 
            case.completed_steps.append("recommendation")
 
        except Exception as exc:
 
            case.errors.append(
                f"recommendation failed: {str(exc)}"
            )
 
 
        # -------------------------------------------------
        # 6. Safety
        # -------------------------------------------------
 
        try:
 
            safety_result = evaluate_safety(
                telemetry=case.telemetry,
                severity=None,
            )
 
            if isinstance(safety_result, bool):
                case.safety_status = (
                    "PASSED" if safety_result else "FAILED"
                )
 
            elif isinstance(safety_result, str):
                case.safety_status = safety_result
 
            elif isinstance(safety_result, dict):
                case.safety_status = safety_result.get(
                    "status",
                    "PASSED"
                )
 
            else:
                case.safety_status = "PASSED"
 
            case.completed_steps.append("safety")
 
        except Exception as exc:
 
            case.safety_status = "FAILED"
 
            case.errors.append(
                f"safety check failed: {str(exc)}"
            )
 
 
        # -------------------------------------------------
        # Final status
        # -------------------------------------------------
 
        if case.safety_status == "FAILED":
            status = "BLOCKED"
 
        elif case.errors:
            status = "COMPLETED_WITH_ERRORS"
 
        else:
            status = "SUCCESS"
 
 
        # -------------------------------------------------
        # Return API response
        # -------------------------------------------------
 
        return TriageResponse(
            status=status,
            case_id=case.case_id,
            asset_id=case.asset_id,
            machine_model=case.machine_model,
            manual_version=case.manual_version,
            alarm=case.alarm,
            selected_tools=case.selected_tools,
            completed_steps=case.completed_steps,
            errors=case.errors,
            rag_evidence=case.rag_evidence,
            maintenance_history=case.maintenance_history,
            telemetry=case.telemetry,
            spare_inventory=case.spare_inventory,
            inventory=case.inventory,
            recommended_action=case.recommended_action,
            safety_status=case.safety_status,
            hitl_status=case.hitl_status,
            work_order=case.work_order,
        )
 
 
    except Exception as exc:
 
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )