import pytest
 
from app.agents.recommender import AgentRecommender
from app.agents.safety import SafetyChecker
 
 
def test_missing_telemetry_does_not_create_fake_temperature():
    recommender = AgentRecommender()
 
    recommendation = recommender.recommend(
        alarm="High temperature alarm",
        telemetry={},
        maintenance_history=[],
        spare_inventory=[],
        rag_evidence=[],
    )
 
    # The recommender must not invent a temperature
    assert recommendation == (
        "Inspect the temperature sensor "
        "and cooling system."
    )
 
 
def test_missing_telemetry_is_not_treated_as_critical():
    safety_checker = SafetyChecker()
 
    result = safety_checker.check(
        telemetry={},
        severity="HIGH",
    )
 
    assert result["passed"] is True
 
    assert result["status"] == "PASSED"
 
    assert result["reasons"] == []
 
 
def test_critical_temperature_blocks_action():
    safety_checker = SafetyChecker()
 
    result = safety_checker.check(
        telemetry={
            "temperature": 105
        },
        severity="HIGH",
    )
 
    assert result["passed"] is False
 
    assert result["status"] == "BLOCKED"
 
    assert (
        "Temperature is above the critical safety limit."
        in result["reasons"]
    )
 
 
def test_critical_vibration_blocks_action():
    safety_checker = SafetyChecker()
 
    result = safety_checker.check(
        telemetry={
            "vibration": 9
        },
        severity="HIGH",
    )
 
    assert result["passed"] is False
 
    assert result["status"] == "BLOCKED"
 
    assert (
        "Vibration is above the critical safety limit."
        in result["reasons"]
    )
 
 
def test_critical_pressure_blocks_action():
    safety_checker = SafetyChecker()
 
    result = safety_checker.check(
        telemetry={
            "pressure": 11
        },
        severity="HIGH",
    )
 
    assert result["passed"] is False
 
    assert result["status"] == "BLOCKED"
 
    assert (
        "Pressure is above the critical safety limit."
        in result["reasons"]
    )
 
 
def test_critical_severity_blocks_action():
    safety_checker = SafetyChecker()
 
    result = safety_checker.check(
        telemetry={
            "temperature": 80
        },
        severity="CRITICAL",
    )
 
    assert result["passed"] is False
 
    assert result["status"] == "BLOCKED"
 
    assert (
        "Incident severity is CRITICAL."
        in result["reasons"]
    )