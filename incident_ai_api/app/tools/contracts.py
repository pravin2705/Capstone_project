from typing import Any, Protocol
 
 
class MaintenanceHistoryTool(Protocol):
    """
    Contract for maintenance history tools.
    """
 
    def get_history(
        self,
        asset_id: str,
    ) -> list[dict[str, Any]]:
        ...
 
 
class TelemetryTool(Protocol):
    """
    Contract for telemetry tools.
    """
 
    def get_telemetry(
        self,
        asset_id: str,
    ) -> dict[str, Any]:
        ...
 
 
class SpareInventoryTool(Protocol):
    """
    Contract for spare inventory tools.
    """
 
    def check_inventory(
        self,
        part_number: str,
    ) -> dict[str, Any]:
        ...
 
 
class RAGKnowledgeTool(Protocol):
    """
    Contract for the Week 2 RAG knowledge tool.
    """
 
    def search_knowledge(
        self,
        query: str,
        machine_model: str,
        manual_version: str | None = None,
    ) -> list[dict[str, Any]]:
        ...
 
 
class WorkOrderTool(Protocol):
    """
    Contract for creating a mock work order.
    """
 
    def create_work_order(
        self,
        case_id: str,
        asset_id: str,
        action: str,
    ) -> dict[str, Any]:
        ...
 