from typing import Any
 
 
class WorkOrderTool:
    """
    Mock work-order system.
 
    A real enterprise API would be called here in production.
    For this project, we use synthetic data only.
    """
 
    def __init__(self):
        self.counter = 0
 
    def create_work_order(
        self,
        case_id: str,
        asset_id: str,
        action: str,
    ) -> dict[str, Any]:
 
        if not case_id:
            raise ValueError("case_id is required")
 
        if not asset_id:
            raise ValueError("asset_id is required")
 
        if not action:
            raise ValueError("action is required")
 
        self.counter += 1
 
        work_order_id = f"WO-{self.counter:03d}"
 
        return {
            "work_order_id": work_order_id,
            "case_id": case_id,
            "asset_id": asset_id,
            "action": action,
            "status": "CREATED",
        }