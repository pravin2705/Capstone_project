from fastapi import FastAPI
 
from app.providers.mock_provider import MockLLMProvider
 
from app.schemas.ai_output import IncidentAIOutput
from app.schemas.incident import IncidentRequest
from app.schemas.rag import RAGRequest, RAGResponse
 
from app.services.incident_service import IncidentService
from app.services.rag_service import RAGService
 
from app.exceptions.handlers import (
    IncidentProcessingError,
    incident_processing_exception_handler,
)
 
# Week 3 routers
from app.api.triage import router as triage_router
from app.api.hitl import router as hitl_router
 
 
app = FastAPI(
    title="Incident AI API",
    description="AI-powered industrial incident intake API",
    version="1.0.0",
)
 
 
# ============================================================
# Exception Handler
# ============================================================
 
app.add_exception_handler(
    IncidentProcessingError,
    incident_processing_exception_handler,
)
 
 
# ============================================================
# Week 1 - Provider / Incident Service
# ============================================================
 
provider = MockLLMProvider()
 
incident_service = IncidentService(provider)
 
 
# ============================================================
# Week 2 - RAG Service
# ============================================================
 
rag_service = RAGService()
 
 
# ============================================================
# Week 1 - Health
# ============================================================
 
@app.get("/health")
def health_check():
 
    return {
        "status": "healthy"
    }
 
 
# ============================================================
# Week 1 - Incident API
# ============================================================
 
@app.post(
    "/incidents",
    response_model=IncidentAIOutput,
)
def create_incident(
    incident: IncidentRequest,
):
 
    return incident_service.process_incident(
        incident
    )
 
 
# ============================================================
# Week 2 - RAG / Maintenance Guidance
# ============================================================
 
@app.post(
    "/maintenance-guidance",
    response_model=RAGResponse,
)
def maintenance_guidance(
    request: RAGRequest,
):
 
    evidence = rag_service.get_maintenance_guidance(
        query=request.query,
        machine_model=request.machine_model,
        manual_version=request.manual_version,
    )
 
    return {
        "query": request.query,
        "machine_model": request.machine_model,
        "manual_version": request.manual_version,
        "evidence": evidence,
    }
 
 
# ============================================================
# Week 3 - Triage API
# ============================================================
 
app.include_router(triage_router)
 
 
# ============================================================
# Week 3 - HITL API
# ============================================================
 
app.include_router(hitl_router)