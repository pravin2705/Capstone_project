from dataclasses import dataclass, field
from typing import Any
 
 
@dataclass
class CaseState:
    """
    Stores the complete state of one incident case.
    """
 
    incident_id: str
    machine_model: str | None = None
    alarm_type: str | None = None
    severity: str | None = None
 
    maintenance_history: list[dict[str, Any]] = field(
        default_factory=list
    )
 
    telemetry: dict[str, Any] = field(
        default_factory=dict
    )
 
    spare_inventory: list[dict[str, Any]] = field(
        default_factory=list
    )
 
    rag_evidence: list[dict[str, Any]] = field(
        default_factory=list
    )
 
    recommended_action: str | None = None
 
    safety_check_passed: bool = False
 
    engineer_approved: bool = False
 
    work_order: dict[str, Any] | None = None
 
    errors: list[str] = field(
        default_factory=list
    )
 
    completed_steps: list[str] = field(
        default_factory=list
    )