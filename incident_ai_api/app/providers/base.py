from abc import ABC, abstractmethod
 
from app.schemas.ai_output import IncidentAIOutput
 
 
class LLMProvider(ABC):
 
    @abstractmethod
    def analyze_incident(
        self,
        incident_data: dict
    ) -> IncidentAIOutput:
        pass