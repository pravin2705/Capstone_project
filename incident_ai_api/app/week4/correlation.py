import uuid
 
 
def generate_correlation_id() -> str:
    return f"CORR-{uuid.uuid4().hex[:12].upper()}"