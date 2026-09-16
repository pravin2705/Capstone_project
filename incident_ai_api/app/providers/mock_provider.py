from app.providers.base import LLMProvider
from app.schemas.ai_output import (
    IncidentAIOutput,
    IncidentType,
    Severity,
)
 
 
class MockLLMProvider(LLMProvider):
 
    def analyze_incident(
        self,
        incident_data: dict
    ) -> IncidentAIOutput:
 
        alarm = incident_data["alarm"].lower()
        description = incident_data["description"].lower()
 
        facts = {
            "asset_id": incident_data["asset_id"],
            "alarm": incident_data["alarm"],
            "description": incident_data["description"],
        }
 
        if "temperature" in alarm or "hot" in description:
            incident_type = IncidentType.OVERHEATING
            severity = Severity.HIGH
 
        elif "vibration" in alarm or "vibrat" in description:
            incident_type = IncidentType.VIBRATION
            severity = Severity.MEDIUM
 
        elif "pressure" in alarm:
            incident_type = IncidentType.HIGH_PRESSURE
            severity = Severity.HIGH
 
        elif "leak" in alarm:
            incident_type = IncidentType.LEAK
            severity = Severity.HIGH
 
        else:
            incident_type = IncidentType.OTHER
            severity = Severity.LOW
 
        summary = (
            f"{incident_data['asset_id']} reported "
            f"{incident_data['alarm']}. "
            f"The incident was classified as "
            f"{incident_type.value} with {severity.value} severity."
        )
 
        return IncidentAIOutput(
            incident_type=incident_type,
            severity=severity,
            facts=facts,
            summary=summary,
        )