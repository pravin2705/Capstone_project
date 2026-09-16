from typing import Any
 
 
# Synthetic maintenance history data
MAINTENANCE_DATA: dict[str, list[dict[str, Any]]] = {
    "PUMP-101": [
        {
            "date": "2026-01-15",
            "issue": "High Temperature Alarm",
            "action": "Cooling fan inspected",
            "technician": "TECH-001",
            "status": "RESOLVED",
        },
        {
            "date": "2026-03-10",
            "issue": "Vibration Alarm",
            "action": "Motor alignment performed",
            "technician": "TECH-002",
            "status": "RESOLVED",
        },
    ],
    "PUMP-102": [
        {
            "date": "2026-02-20",
            "issue": "Pressure Alarm",
            "action": "Pressure sensor inspected",
            "technician": "TECH-003",
            "status": "RESOLVED",
        }
    ],
}
 
 
def get_maintenance_history(
    asset_id: str,
) -> list[dict[str, Any]]:
    """
    Mock maintenance history tool.
 
    Returns previous maintenance records
    for the requested asset.
    """
 
    return MAINTENANCE_DATA.get(asset_id, [])