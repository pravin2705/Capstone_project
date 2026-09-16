from app.tools.telemetry import get_telemetry
 
 
def test_get_telemetry():
    result = get_telemetry("PUMP-101")
 
    assert result["temperature"] == 95.0
    assert result["vibration"] == 2.1
    assert result["pressure"] == 4.5
    assert result["status"] == "RUNNING"
 
 
def test_unknown_asset():
    result = get_telemetry("UNKNOWN-ASSET")
 
    assert result == {}