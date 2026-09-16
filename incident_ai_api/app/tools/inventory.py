from typing import Any
 
 
# Synthetic spare inventory data
INVENTORY_DATA: dict[str, dict[str, Any]] = {
    "CF-PX500-001": {
        "part_number": "CF-PX500-001",
        "part_name": "Cooling Fan",
        "quantity": 3,
        "status": "AVAILABLE",
    },
    "TS-PX500-002": {
        "part_number": "TS-PX500-002",
        "part_name": "Temperature Sensor",
        "quantity": 2,
        "status": "AVAILABLE",
    },
    "CF-PX700-001": {
        "part_number": "CF-PX700-001",
        "part_name": "Cooling Fan",
        "quantity": 0,
        "status": "OUT_OF_STOCK",
    },
}
 
 
def check_inventory(
    part_number: str,
) -> dict[str, Any]:
    """
    Mock spare inventory tool.
 
    Returns inventory information for
    the requested spare part.
    """
 
    return INVENTORY_DATA.get(
        part_number,
        {
            "part_number": part_number,
            "part_name": "UNKNOWN",
            "quantity": 0,
            "status": "NOT_FOUND",
        },
    )
 