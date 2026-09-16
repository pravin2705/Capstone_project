import pytest
 
from app.tools.work_order import WorkOrderTool
 
 
def test_create_work_order():
 
    tool = WorkOrderTool()
 
    result = tool.create_work_order(
        case_id="CASE-001",
        asset_id="PUMP-101",
        action="Inspect cooling system",
    )
 
    assert result["work_order_id"] == "WO-001"
    assert result["case_id"] == "CASE-001"
    assert result["asset_id"] == "PUMP-101"
    assert result["action"] == "Inspect cooling system"
    assert result["status"] == "CREATED"
 
 
def test_create_multiple_work_orders():
 
    tool = WorkOrderTool()
 
    first = tool.create_work_order(
        case_id="CASE-001",
        asset_id="PUMP-101",
        action="Inspect cooling system",
    )
 
    second = tool.create_work_order(
        case_id="CASE-002",
        asset_id="PUMP-102",
        action="Inspect pressure system",
    )
 
    assert first["work_order_id"] == "WO-001"
    assert second["work_order_id"] == "WO-002"
 
 
def test_missing_case_id():
 
    tool = WorkOrderTool()
 
    with pytest.raises(ValueError):
 
        tool.create_work_order(
            case_id="",
            asset_id="PUMP-101",
            action="Inspect cooling system",
        )
 
 
def test_missing_asset_id():
 
    tool = WorkOrderTool()
 
    with pytest.raises(ValueError):
 
        tool.create_work_order(
            case_id="CASE-001",
            asset_id="",
            action="Inspect cooling system",
        )
 
 
def test_missing_action():
 
    tool = WorkOrderTool()
 
    with pytest.raises(ValueError):
 
        tool.create_work_order(
            case_id="CASE-001",
            asset_id="PUMP-101",
            action="",
        )
 