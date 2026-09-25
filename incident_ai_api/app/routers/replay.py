from fastapi import APIRouter, HTTPException
 
from app.week4.models import (
    ReplayRequest,
    ReplayComparison,
)
 
from app.week4.replay import (
    load_checkpoint,
    merge_evidence,
)
 
from app.agents.recommender import AgentRecommender
from app.agents.safety import SafetyChecker
 
from app.week4.correlation import generate_correlation_id
from app.week4.audit import record_audit_event
 
 
router = APIRouter(
    prefix="/replay",
    tags=["Week 4 - Replay"],
)
 
 
recommender = AgentRecommender()
safety_checker = SafetyChecker()
 
 
@router.post(
    "/{case_id}",
    response_model=ReplayComparison,
)
def replay_case(
    case_id: str,
    request: ReplayRequest,
):
    # ---------------------------------------------------------
    # 1. Load previous checkpoint
    # ---------------------------------------------------------
    try:
        checkpoint = load_checkpoint(
            case_id
        )
 
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
 
    # ---------------------------------------------------------
    # 2. Generate new correlation ID
    # ---------------------------------------------------------
    correlation_id = generate_correlation_id()
 
    record_audit_event(
        correlation_id=correlation_id,
        case_id=case_id,
        event_type="REPLAY_STARTED",
        component="ReplayAPI",
        status="STARTED",
        details={
            "new_evidence":
                request.new_evidence,
        },
    )
 
    try:
        # -----------------------------------------------------
        # 3. Merge old evidence + new evidence
        # -----------------------------------------------------
        updated_evidence = merge_evidence(
            checkpoint.evidence,
            request.new_evidence,
        )
 
        # -----------------------------------------------------
        # 4. Get replay telemetry
        # -----------------------------------------------------
        telemetry = updated_evidence.get(
            "telemetry",
            {},
        )
 
        # -----------------------------------------------------
        # 5. Get other evidence
        # -----------------------------------------------------
        maintenance_history = (
            updated_evidence.get(
                "maintenance_history",
                [],
            )
        )
 
        inventory = updated_evidence.get(
            "inventory",
            [],
        )
 
        rag_evidence = updated_evidence.get(
            "rag_evidence",
            [],
        )
 
        # -----------------------------------------------------
        # 6. Rerun recommendation
        # -----------------------------------------------------
        replayed_recommendation = (
            recommender.recommend(
                alarm=checkpoint.incident.get(
                    "alarm",
                    "",
                ),
                telemetry=telemetry,
                maintenance_history=(
                    maintenance_history
                ),
                spare_inventory=inventory,
                rag_evidence=rag_evidence,
            )
        )
 
        record_audit_event(
            correlation_id=correlation_id,
            case_id=case_id,
            event_type="REPLAY_RECOMMENDATION_GENERATED",
            component="AgentRecommender",
            status="SUCCESS",
            details={
                "original_recommendation":
                    checkpoint.recommendation,
                "replayed_recommendation":
                    replayed_recommendation,
                "telemetry":
                    telemetry,
            },
        )
 
        # -----------------------------------------------------
        # 7. Run safety check on replay evidence
        # -----------------------------------------------------
        safety_result = safety_checker.check(
            telemetry=telemetry,
            severity="HIGH",
        )
 
        if isinstance(
            safety_result,
            dict,
        ):
            safety_passed = safety_result.get(
                "passed",
                False,
            )
        elif isinstance(
            safety_result,
            bool,
        ):
            safety_passed = safety_result
        else:
            safety_passed = True
 
        # -----------------------------------------------------
        # 8. Compare recommendations
        # -----------------------------------------------------
        recommendation_changed = (
            checkpoint.recommendation
            != replayed_recommendation
        )
 
        # -----------------------------------------------------
        # 9. Explain change
        # -----------------------------------------------------
        if recommendation_changed:
 
            explanation = (
                "The recommendation changed because "
                "the replay used updated evidence. "
                "The replayed recommendation was "
                "generated using the latest telemetry "
                "and available maintenance evidence."
            )
 
        else:
 
            explanation = (
                "The recommendation did not change "
                "because the new evidence did not "
                "change the recommendation logic."
            )
 
        # -----------------------------------------------------
        # 10. Safety explanation
        # -----------------------------------------------------
        if not safety_passed:
 
            explanation += (
                " Replay safety checks did not pass, "
                "so the recommendation must not be "
                "treated as automatically executable."
            )
 
        # -----------------------------------------------------
        # 11. Audit replay completion
        # -----------------------------------------------------
        record_audit_event(
            correlation_id=correlation_id,
            case_id=case_id,
            event_type="REPLAY_COMPLETED",
            component="ReplayAPI",
            status=(
                "SUCCESS"
                if safety_passed
                else "BLOCKED"
            ),
            details={
                "recommendation_changed":
                    recommendation_changed,
                "original_recommendation":
                    checkpoint.recommendation,
                "replayed_recommendation":
                    replayed_recommendation,
                "safety_result":
                    safety_result,
            },
        )
 
        # -----------------------------------------------------
        # 12. Return comparison
        # -----------------------------------------------------
        return ReplayComparison(
            case_id=case_id,
            original_recommendation=(
                checkpoint.recommendation
            ),
            replayed_recommendation=(
                replayed_recommendation
            ),
            recommendation_changed=(
                recommendation_changed
            ),
            original_evidence=(
                checkpoint.evidence
            ),
            new_evidence=(
                request.new_evidence
            ),
            explanation=explanation,
        )
 
    except Exception as exc:
 
        record_audit_event(
            correlation_id=correlation_id,
            case_id=case_id,
            event_type="REPLAY_FAILED",
            component="ReplayAPI",
            status="FAILED",
            details={
                "error": str(exc),
            },
        )
 
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
 