from pydantic import BaseModel
from typing import Optional
 
 
class DocumentMetadata(BaseModel):
    file_name: str
    machine_model: Optional[str] = None
    manual_version: Optional[str] = None
    document_type: str
    section: Optional[str] = None
    page: Optional[int] = None
 
 
class DocumentChunk(BaseModel):
    chunk_id: str
    text: str
    metadata: DocumentMetadata