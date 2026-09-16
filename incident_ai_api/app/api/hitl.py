from fastapi import APIRouter, HTTPException
 
from app.schemas.case_state import CaseState
from app.workflow.hitl import EngineerHITL
from app.workflow.work_order_gate import WorkOrderGate
 
 
router = APIRouter(
    prefix="/hitl",
    tags=["HITL"],
)
 
 
# In-memory case storage for Week 3
CASES: dict[str, CaseState] = {}
 
 
@router.post("/{case_id}/request")
def request_approval(case_id: str):
    """
    Create an HITL approval request for an existing case.
    """
 
    case = CASES.get(case_id)
 
    if case is None:
        raise HTTPException(
            status_code=404,
            detail=f"Case '{case_id}' not found",
        )
 
    hitl = EngineerHITL()
 
    hitl.request_approval(case)
 
    return {
        "case_id": case.case_id,
        "hitl_status": case.hitl_status,
        "message": "Engineer approval requested",
    }
 
 
@router.post("/{case_id}/approve")
def approve_case(case_id: str):
    """
    Record engineer approval for a case.
    """
 
    case = CASES.get(case_id)
 
    if case is None:
        raise HTTPException(
            status_code=404,
            detail=f"Case '{case_id}' not found",
        )
 
    hitl = EngineerHITL()
 
    hitl.approve(case)
 
    return {
        "case_id": case.case_id,
        "hitl_status": case.hitl_status,
        "message": "Engineer approval recorded",
    }
 
 
@router.post("/{case_id}/reject")
def reject_case(case_id: str):
    """
    Record engineer rejection for a case.
    """
 
    case = CASES.get(case_id)
 
    if case is None:
        raise HTTPException(
            status_code=404,
            detail=f"Case '{case_id}' not found",
        )
 
    hitl = EngineerHITL()
 
    hitl.reject(case)
 
    return {
        "case_id": case.case_id,
        "hitl_status": case.hitl_status,
        "message": "Engineer rejection recorded",
    }
 
 
@router.get("/{case_id}")
def get_hitl_status(case_id: str):
    """
    Get current HITL status of a case.
    """
 
    case = CASES.get(case_id)
 
    if case is None:
        raise HTTPException(
            status_code=404,
            detail=f"Case '{case_id}' not found",
        )
 
    return {
        "case_id": case.case_id,
        "hitl_status": case.hitl_status,
        "safety_status": case.safety_status,
        "recommended_action": case.recommended_action,
    }