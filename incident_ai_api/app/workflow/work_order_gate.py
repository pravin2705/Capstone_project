from typing import Any
 
from app.schemas.case_state import CaseState
from app.tools.work_order import WorkOrderTool
 
 
class WorkOrderGate:
    """
    Controls work-order creation.
 
    A work order can only be created when:
    1. Safety check has passed.
    2. Engineer has approved the recommendation.
    3. Required case information is available.
    """
 
    def __init__(
        self,
        work_order_tool: WorkOrderTool | None = None,
    ):
        self.work_order_tool = (
            work_order_tool or WorkOrderTool()
        )
 
    def create_if_approved(
        self,
        case: CaseState,
    ) -> dict[str, Any]:
 
        # -------------------------------------------------
        # Safety gate
        # -------------------------------------------------
 
        if case.safety_status != "PASSED":
            return {
                "status": "BLOCKED",
                "reason": (
                    "Work order creation blocked because "
                    "the safety check has not passed."
                ),
                "work_order": None,
            }
 
        # -------------------------------------------------
        # Engineer HITL gate
        # -------------------------------------------------
 
        if case.hitl_status != "APPROVED":
            return {
                "status": "BLOCKED",
                "reason": (
                    "Work order creation requires "
                    "engineer approval."
                ),
                "work_order": None,
            }
 
        # -------------------------------------------------
        # Required input validation
        # -------------------------------------------------
 
        if not case.case_id:
            return {
                "status": "BLOCKED",
                "reason": "case_id is required.",
                "work_order": None,
            }
 
        if not case.asset_id:
            return {
                "status": "BLOCKED",
                "reason": "asset_id is required.",
                "work_order": None,
            }
 
        if not case.recommended_action:
            return {
                "status": "BLOCKED",
                "reason": (
                    "recommended_action is required."
                ),
                "work_order": None,
            }
 
        # -------------------------------------------------
        # Create mock work order
        # -------------------------------------------------
 
        work_order = (
            self.work_order_tool.create_work_order(
                case_id=case.case_id,
                asset_id=case.asset_id,
                action=case.recommended_action,
            )
        )
 
        case.work_order = work_order
 
        if "work_order_created" not in case.completed_steps:
            case.completed_steps.append(
                "work_order_created"
            )
 
        return {
            "status": "CREATED",
            "reason": (
                "Engineer approved the recommendation "
                "and safety check passed."
            ),
            "work_order": work_order,
        }