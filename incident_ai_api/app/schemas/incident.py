from pydantic import BaseModel, Field
 
 
class IncidentRequest(BaseModel):
    asset_id: str = Field(..., min_length=1)
    alarm: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
 
    temperature: float | None = None
    pressure: float | None = None
    vibration: float | None = None