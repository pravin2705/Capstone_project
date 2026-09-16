from typing import Any
from pydantic import BaseModel, Field
 
 
class CaseState(BaseModel):
    """
    Shared state for the Week 3 Agentic Triage workflow.
    """
 
    # ---------------------------------------------------------
    # Basic case information
    # ---------------------------------------------------------
 
    case_id: str
    asset_id: str
    machine_model: str
    manual_version: str | None = None
    alarm: str
 
    # ---------------------------------------------------------
    # Agent / workflow state
    # ---------------------------------------------------------
 
    selected_tools: list[str] = Field(default_factory=list)
 
    completed_steps: list[str] = Field(default_factory=list)
 
    errors: list[str] = Field(default_factory=list)
 
    # ---------------------------------------------------------
    # RAG evidence
    # ---------------------------------------------------------
 
    rag_evidence: list[Any] = Field(default_factory=list)
 
    # ---------------------------------------------------------
    # Maintenance history
    # ---------------------------------------------------------
 
    maintenance_history: list[Any] = Field(default_factory=list)
 
    # ---------------------------------------------------------
    # Telemetry
    # ---------------------------------------------------------
 
    telemetry: dict[str, Any] | None = None
 
    # ---------------------------------------------------------
    # Spare inventory
    # ---------------------------------------------------------
 
    spare_inventory: list[Any] = Field(default_factory=list)
 
    # Keep inventory also for compatibility
    inventory: list[Any] = Field(default_factory=list)
 
    # ---------------------------------------------------------
    # Recommendation
    # ---------------------------------------------------------
 
    recommended_action: str | None = None
 
    # ---------------------------------------------------------
    # Safety
    # ---------------------------------------------------------
 
    safety_status: str = "NOT_CHECKED"
 
    # ---------------------------------------------------------
    # Human-in-the-loop
    # ---------------------------------------------------------
 
    hitl_status: str = "PENDING"
 
    # ---------------------------------------------------------
    # Work order
    # ---------------------------------------------------------
 
    work_order: dict[str, Any] | None = None