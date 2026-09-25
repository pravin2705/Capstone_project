import json
from datetime import datetime, timezone
from pathlib import Path
 
from app.week4.models import AuditEvent
 
 
AUDIT_DIR = Path("data/audit")
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
 
 
def record_audit_event(
    correlation_id: str,
    case_id: str,
    event_type: str,
    component: str,
    status: str,
    details: dict | None = None,
):
    event = AuditEvent(
        correlation_id=correlation_id,
        case_id=case_id,
        event_type=event_type,
        component=component,
        timestamp=datetime.now(timezone.utc).isoformat(),
        status=status,
        details=details or {},
    )
 
    audit_file = AUDIT_DIR / f"{case_id}.jsonl"
 
    with audit_file.open("a", encoding="utf-8") as file:
        file.write(
            json.dumps(event.model_dump()) + "\n"
        )
 
    return event
 