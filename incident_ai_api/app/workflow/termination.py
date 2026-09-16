from app.schemas.case_state import CaseState
 
 
class WorkflowTerminator:
    """
    Determines whether the investigation can stop.
    """
 
    REQUIRED_STEPS = {
        "rag",
        "maintenance",
        "telemetry",
        "recommendation",
        "safety",
    }
 
    def should_terminate(
        self,
        case: CaseState,
    ) -> bool:
        """
        Return True when the investigation has
        collected enough information.
        """
 
        completed = set(case.completed_steps)
 
        return self.REQUIRED_STEPS.issubset(completed)
 
    def termination_reason(
        self,
        case: CaseState,
    ) -> str:
        """
        Explain why the workflow can or cannot stop.
        """
 
        if self.should_terminate(case):
            return (
                "Investigation complete. "
                "Safety check completed. "
                "Engineer approval is required before "
                "work-order creation."
            )
 
        completed = set(case.completed_steps)
 
        missing = self.REQUIRED_STEPS - completed
 
        return (
            "Investigation is not complete. "
            f"Missing steps: {sorted(missing)}"
        )