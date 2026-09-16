from typing import Any
 
 
# Synthetic telemetry data
TELEMETRY_DATA: dict[str, dict[str, Any]] = {
    "PUMP-101": {
        "temperature": 95.0,
        "vibration": 2.1,
        "pressure": 4.5,
        "status": "RUNNING",
    },
    "PUMP-102": {
        "temperature": 78.0,
        "vibration": 1.8,
        "pressure": 5.2,
        "status": "RUNNING",
    },
}
 
 
def get_telemetry(
    asset_id: str,
) -> dict[str, Any]:
    """
    Mock telemetry tool.
 
    Returns current telemetry information
    for the requested asset.
    """
 
    return TELEMETRY_DATA.get(asset_id, {})