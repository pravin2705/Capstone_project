from typing import Any
 
 
class AgentRecommender:
    """
    Generates a deterministic recommendation
    using information collected by the tools.
    """
 
    def recommend(
        self,
        alarm: str,
        telemetry: dict[str, Any],
        maintenance_history: list[dict[str, Any]],
        spare_inventory: list[dict[str, Any]],
        rag_evidence: list[dict[str, Any]],
    ) -> str:
 
        alarm_lower = alarm.lower()
 
        temperature = telemetry.get("temperature")
 
        # High temperature scenario
        if (
            "temperature" in alarm_lower
            or "overheat" in alarm_lower
        ):
 
            if (
                temperature is not None
                and temperature >= 90
            ):
                return (
                    "Inspect the cooling system, "
                    "cooling fan and temperature sensor."
                )
 
            return (
                "Inspect the temperature sensor "
                "and cooling system."
            )
 
        # Vibration scenario
        if "vibration" in alarm_lower:
 
            return (
                "Inspect motor alignment, bearings "
                "and vibration source."
            )
 
        # Pressure scenario
        if "pressure" in alarm_lower:
 
            return (
                "Inspect pressure sensor, valve "
                "and pressure control system."
            )
 
        # Leak scenario
        if "leak" in alarm_lower:
 
            return (
                "Inspect the affected piping, "
                "connections and seals."
            )
 
        return (
            "Perform further investigation using "
            "maintenance history and telemetry."
        )