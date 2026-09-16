from app.schemas.case_state import CaseState
 
 
class EngineerHITL:
    """
    Handles engineer approval before a work order
    can be created.
    """
 
    def request_approval(
        self,
        case: CaseState,
    ) -> dict[str, str]:
        """
        Prepare an approval request for the engineer.
        """
 
        return {
            "case_id": case.case_id,
            "asset_id": case.asset_id or "",
            "recommendation": (
                case.recommended_action or ""
            ),
            "safety_status": case.safety_status,
            "status": "PENDING",
        }
 
    def approve(
        self,
        case: CaseState,
    ) -> CaseState:
        """
        Record engineer approval.
        """
 
        if case.safety_status != "PASSED":
            raise ValueError(
                "Engineer approval cannot proceed "
                "because the safety check has not passed."
            )
 
        case.hitl_status = "APPROVED"
 
        if "hitl_approved" not in case.completed_steps:
            case.completed_steps.append(
                "hitl_approved"
            )
 
        return case
 
    def reject(
        self,
        case: CaseState,
    ) -> CaseState:
        """
        Record engineer rejection.
        """
 
        case.hitl_status = "REJECTED"
 
        if "hitl_rejected" not in case.completed_steps:
            case.completed_steps.append(
                "hitl_rejected"
            )
 
        return case