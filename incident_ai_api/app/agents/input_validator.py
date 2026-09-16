from app.schemas.case_state import CaseState
 
 
class IncidentInputValidator:
    """
    Validates the minimum information required
    before starting agent investigation.
    """
 
    REQUIRED_FIELDS = [
        "case_id",
        "asset_id",
        "machine_model",
        "alarm",
    ]
 
    def validate(
        self,
        case: CaseState,
    ) -> dict[str, object]:
        """
        Validate the current case.
 
        Returns a structured validation result
        instead of raising an exception.
        """
 
        missing_fields: list[str] = []
 
        for field in self.REQUIRED_FIELDS:
            value = getattr(case, field, None)
 
            if value is None or str(value).strip() == "":
                missing_fields.append(field)
 
        if missing_fields:
            return {
                "valid": False,
                "status": "INCOMPLETE",
                "missing_fields": missing_fields,
                "message": (
                    "Required incident information is missing."
                ),
            }
 
        return {
            "valid": True,
            "status": "VALID",
            "missing_fields": [],
            "message": "Incident input is complete.",
        }