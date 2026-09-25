import json
from datetime import datetime, timezone
from pathlib import Path
 
from app.week4.models import Checkpoint
 
 
CHECKPOINT_DIR = Path("data/checkpoints")
CHECKPOINT_DIR.mkdir(
    parents=True,
    exist_ok=True
)
 
 
def save_checkpoint(
    case_id: str,
    correlation_id: str,
    incident: dict,
    evidence: dict,
    recommendation: str | None,
    reasoning: str | None,
    status: str,
) -> Checkpoint:
 
    checkpoint = Checkpoint(
        case_id=case_id,
        correlation_id=correlation_id,
        created_at=datetime.now(
            timezone.utc
        ).isoformat(),
        incident=incident,
        evidence=evidence,
        recommendation=recommendation,
        reasoning=reasoning,
        status=status,
    )
 
    checkpoint_file = (
        CHECKPOINT_DIR / f"{case_id}.json"
    )
 
    checkpoint_file.write_text(
        json.dumps(
            checkpoint.model_dump(),
            indent=2
        ),
        encoding="utf-8",
    )
 
    return checkpoint
 
 
def load_checkpoint(case_id: str) -> Checkpoint:
 
    checkpoint_file = (
        CHECKPOINT_DIR / f"{case_id}.json"
    )
 
    if not checkpoint_file.exists():
        raise FileNotFoundError(
            f"No checkpoint found for {case_id}"
        )
 
    data = json.loads(
        checkpoint_file.read_text(
            encoding="utf-8"
        )
    )
 
    return Checkpoint.model_validate(data)
def merge_evidence(
    original: dict,
    new_evidence: dict
) -> dict:
 
    merged = original.copy()
 
    for key, value in new_evidence.items():
        merged[key] = value
 
    return merged