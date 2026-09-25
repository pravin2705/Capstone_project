def test_week4_correlation_id_format():
    from app.week4.correlation import (
        generate_correlation_id,
    )
 
    correlation_id = generate_correlation_id()
 
    assert correlation_id.startswith("CORR-")
    assert len(correlation_id) > 10
 
 
def test_week4_evaluation_success():
 
    from app.week4.evaluation import (
        evaluate_tool_result,
    )
 
    result = evaluate_tool_result(
        "TelemetryTool",
        {"temperature": 75},
    )
 
    assert result["status"] == "PASS"
 
 
def test_week4_evaluation_failure():
 
    from app.week4.evaluation import (
        evaluate_tool_result,
    )
 
    result = evaluate_tool_result(
        "TelemetryTool",
        None,
    )
 
    assert result["status"] == "FAIL"