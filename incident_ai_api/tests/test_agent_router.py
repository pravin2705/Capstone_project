from app.agents.router import AgentRouter
 
 
def test_temperature_alarm_routing():
 
    router = AgentRouter()
 
    tools = router.select_tools(
        "High Temperature Alarm"
    )
 
    assert "rag" in tools
    assert "maintenance" in tools
    assert "telemetry" in tools
    assert "inventory" in tools
 
 
def test_vibration_alarm_routing():
 
    router = AgentRouter()
 
    tools = router.select_tools(
        "Vibration Alarm"
    )
 
    assert "rag" in tools
    assert "maintenance" in tools
    assert "telemetry" in tools
    assert "inventory" not in tools
 
 
def test_pressure_alarm_routing():
 
    router = AgentRouter()
 
    tools = router.select_tools(
        "High Pressure Alarm"
    )
 
    assert "rag" in tools
    assert "maintenance" in tools
    assert "telemetry" in tools