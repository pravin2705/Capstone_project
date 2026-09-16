from enum import Enum
 
from pydantic import BaseModel, Field
 
 
class IncidentType(str, Enum):
    OVERHEATING = "OVERHEATING"
    VIBRATION = "VIBRATION"
    HIGH_PRESSURE = "HIGH_PRESSURE"
    LEAK = "LEAK"
    MOTOR_FAILURE = "MOTOR_FAILURE"
    OTHER = "OTHER"
 
 
class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
 
 
class IncidentAIOutput(BaseModel):
    incident_type: IncidentType
    severity: Severity
    facts: dict[str, str] = Field(default_factory=dict)
    summary: str = Field(..., min_length=1)
 