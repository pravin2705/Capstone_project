from typing import Any
 
from pydantic import BaseModel, Field
 
 
class AuditEvent(BaseModel):
    correlation_id: str
    case_id: str
    event_type: str
    component: str
    timestamp: str
    status: str
    details: dict[str, Any] = Field(default_factory=dict)
 
 
class Checkpoint(BaseModel):
    case_id: str
    correlation_id: str
    created_at: str
 
    incident: dict[str, Any]
    evidence: dict[str, Any] = Field(default_factory=dict)
 
    recommendation: str | None = None
    reasoning: str | None = None
 
    status: str
 
 
class ReplayRequest(BaseModel):
    case_id: str
 
    new_evidence: dict[str, Any] = Field(
        default_factory=dict
    )
 
 
class ReplayComparison(BaseModel):
    case_id: str
    original_recommendation: str | None
    replayed_recommendation: str | None
 
    recommendation_changed: bool
 
    original_evidence: dict[str, Any]
    new_evidence: dict[str, Any]
 
    explanation: str