from app.tools.contracts import (
    MaintenanceHistoryTool,
    TelemetryTool,
    SpareInventoryTool,
    RAGKnowledgeTool,
    WorkOrderTool,
)
 
 
def test_tool_contracts_exist():
 
    assert MaintenanceHistoryTool is not None
    assert TelemetryTool is not None
    assert SpareInventoryTool is not None
    assert RAGKnowledgeTool is not None
    assert WorkOrderTool is not None