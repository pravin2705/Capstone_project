from fastapi import Request
from fastapi.responses import JSONResponse
 
 
class IncidentProcessingError(Exception):
    def __init__(self, message: str):
        self.message = message
 
 
async def incident_processing_exception_handler(
    request: Request,
    exc: IncidentProcessingError
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Incident processing failed",
            "detail": exc.message
        }
    )