from pydantic import BaseModel
 
 
class TriageRequest(BaseModel):
    case_id: str
    asset_id: str
    machine_model: str
    alarm: str
    manual_version: str | None = None
 
 
class TriageResponse(BaseModel):
    case_id: str
    status: str
    recommended_action: str | None = None
    safety_status: str
    hitl_status: str
    errors: list[str] = []