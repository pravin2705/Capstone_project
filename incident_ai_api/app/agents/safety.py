from typing import Any
 
 
class SafetyChecker:
    """
    Deterministic safety rules for incident triage.
 
    These rules do not depend on an LLM.
    """
 
    CRITICAL_TEMPERATURE = 100.0
    CRITICAL_VIBRATION = 8.0
    CRITICAL_PRESSURE = 10.0
 
    def check(
        self,
        telemetry: dict[str, Any],
        severity: str,
    ) -> dict[str, Any]:
        """
        Check whether the incident can proceed
        to recommendation and human review.
        """
 
        reasons: list[str] = []
 
        temperature = telemetry.get("temperature")
        vibration = telemetry.get("vibration")
        pressure = telemetry.get("pressure")
 
        # Critical temperature
        if (
            temperature is not None
            and temperature >= self.CRITICAL_TEMPERATURE
        ):
            reasons.append(
                "Temperature is above the critical safety limit."
            )
 
        # Critical vibration
        if (
            vibration is not None
            and vibration >= self.CRITICAL_VIBRATION
        ):
            reasons.append(
                "Vibration is above the critical safety limit."
            )
 
        # Critical pressure
        if (
            pressure is not None
            and pressure >= self.CRITICAL_PRESSURE
        ):
            reasons.append(
                "Pressure is above the critical safety limit."
            )
 
        # Critical severity
        if severity.upper() == "CRITICAL":
            reasons.append(
                "Incident severity is CRITICAL."
            )
 
        if reasons:
            return {
                "passed": False,
                "status": "BLOCKED",
                "reasons": reasons,
            }
 
        return {
            "passed": True,
            "status": "PASSED",
            "reasons": [],
        }
 