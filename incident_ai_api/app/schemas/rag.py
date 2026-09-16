from pydantic import BaseModel, Field
 
 
class RAGRequest(BaseModel):
 
    machine_model: str = Field(
        ...,
        description="Machine model, for example PX-500"
    )
 
    manual_version: str = Field(
        ...,
        description="Manual version, for example 3.2"
    )
 
    query: str = Field(
        ...,
        description="Maintenance question"
    )
 
 
class Citation(BaseModel):
 
    source: str
    machine_model: str
    manual_version: str
    section: str | None = None
    chunk_id: str
 
 
class Evidence(BaseModel):
 
    text: str
    score: float
    citation: Citation
 
 
class RAGResponse(BaseModel):
 
    query: str
    machine_model: str
    manual_version: str
    evidence: list[Evidence]