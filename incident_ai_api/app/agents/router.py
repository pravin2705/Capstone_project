class AgentRouter:
    """
    Determines which tools should be used
    for a particular incident.
    """
 
    def select_tools(self, alarm: str) -> list[str]:
        """
        Select tools based on the alarm type.
        """
 
        alarm_lower = alarm.lower()
 
        # Every incident should use RAG
        # and maintenance history.
        tools = [
            "rag",
            "maintenance",
        ]
 
        # Temperature-related incidents
        if "temperature" in alarm_lower or "overheat" in alarm_lower:
            tools.append("telemetry")
            tools.append("inventory")
 
        # Vibration-related incidents
        elif "vibration" in alarm_lower:
            tools.append("telemetry")
 
        # Pressure-related incidents
        elif "pressure" in alarm_lower:
            tools.append("telemetry")
 
        # Leak-related incidents
        elif "leak" in alarm_lower:
            tools.append("telemetry")
            tools.append("inventory")
 
        # Unknown incidents
        else:
            tools.append("telemetry")
 
        return tools