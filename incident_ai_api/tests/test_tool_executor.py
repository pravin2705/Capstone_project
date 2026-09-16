import time
 
import pytest
 
from app.services.tool_executor import (
    ToolExecutionError,
    ToolExecutor,
)
 
 
def test_tool_success():
 
    executor = ToolExecutor(max_retries=2)
 
    def successful_tool():
        return {"status": "success"}
 
    result = executor.execute(successful_tool)
 
    assert result["status"] == "success"
 
 
def test_tool_retry():
 
    executor = ToolExecutor(max_retries=2)
 
    attempts = {"count": 0}
 
    def failing_then_successful_tool():
 
        attempts["count"] += 1
 
        if attempts["count"] < 2:
            raise RuntimeError("Temporary failure")
 
        return {"status": "success"}
 
    result = executor.execute(
        failing_then_successful_tool
    )
 
    assert result["status"] == "success"
    assert attempts["count"] == 2
 
 
def test_tool_failure_after_retries():
 
    executor = ToolExecutor(max_retries=2)
 
    def failing_tool():
        raise RuntimeError("Tool unavailable")
 
    with pytest.raises(ToolExecutionError):
 
        executor.execute(failing_tool)
 
 
def test_tool_timeout():
 
    executor = ToolExecutor(
        max_retries=1,
        timeout_seconds=0.1,
    )
 
    def slow_tool():
 
        time.sleep(1)
 
        return {"status": "success"}
 
    with pytest.raises(ToolExecutionError):
 
        executor.execute(slow_tool)