from app.agents.safety import SafetyChecker
 
 
def test_safe_telemetry():
 
    checker = SafetyChecker()
 
    result = checker.check(
        telemetry={
            "temperature": 85.0,
            "vibration": 2.1,
            "pressure": 4.5,
        },
        severity="HIGH",
    )
 
    assert result["passed"] is True
    assert result["status"] == "PASSED"
 
 
def test_critical_temperature():
 
    checker = SafetyChecker()
 
    result = checker.check(
        telemetry={
            "temperature": 105.0,
            "vibration": 2.1,
            "pressure": 4.5,
        },
        severity="HIGH",
    )
 
    assert result["passed"] is False
    assert result["status"] == "BLOCKED"
 
 
def test_critical_severity():
 
    checker = SafetyChecker()
 
    result = checker.check(
        telemetry={
            "temperature": 85.0,
            "vibration": 2.1,
            "pressure": 4.5,
        },
        severity="CRITICAL",
    )
 
    assert result["passed"] is False
    assert result["status"] == "BLOCKED"