from app.tools.maintenance import get_maintenance_history
 
 
def test_get_maintenance_history():
    result = get_maintenance_history("PUMP-101")
 
    assert len(result) == 2
 
    assert result[0]["issue"] == "High Temperature Alarm"
    assert result[0]["status"] == "RESOLVED"
 
 
def test_unknown_asset():
    result = get_maintenance_history("UNKNOWN-ASSET")
 
    assert result == []