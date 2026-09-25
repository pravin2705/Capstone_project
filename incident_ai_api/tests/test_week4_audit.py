from app.week4.audit import record_audit_event
 
 
def test_record_audit_event(tmp_path, monkeypatch):
    import app.week4.audit as audit_module
 
    test_audit_dir = tmp_path / "audit"
 
    monkeypatch.setattr(
        audit_module,
        "AUDIT_DIR",
        test_audit_dir,
    )
 
    test_audit_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
 
    event = record_audit_event(
        correlation_id="CORR-TEST123456",
        case_id="CASE-TEST",
        event_type="TEST_EVENT",
        component="TestComponent",
        status="SUCCESS",
        details={
            "message": "test"
        },
    )
 
    assert event.correlation_id == "CORR-TEST123456"
    assert event.case_id == "CASE-TEST"
    assert event.event_type == "TEST_EVENT"
 
    audit_file = test_audit_dir / "CASE-TEST.jsonl"
 
    assert audit_file.exists()
 
    content = audit_file.read_text(
        encoding="utf-8"
    )
 
    assert "TEST_EVENT" in content