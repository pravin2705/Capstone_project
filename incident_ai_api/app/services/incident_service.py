from app.providers.base import LLMProvider
from app.schemas.ai_output import IncidentAIOutput
from app.schemas.incident import IncidentRequest
 
 
class IncidentService:
 
    def __init__(self, provider: LLMProvider):
        self.provider = provider
 
    def process_incident(
        self,
        incident: IncidentRequest
    ) -> IncidentAIOutput:
 
        incident_data = incident.model_dump()
 
        return self.provider.analyze_incident(
            incident_data
        )
 