from typing import Any
 
from app.agents.recommender import AgentRecommender
from app.agents.safety import SafetyChecker
 
 
def evaluate_tool_result(
    tool_name: str,
    result: Any,
) -> dict[str, Any]:
    """
    Evaluate the result returned by an enterprise tool.
 
    Deterministic evaluation rules:
 
    PASS:
    - Tool result is not None.
    - Result does not contain an obvious error.
    - Result contains meaningful content.
 
    FAIL:
    - Result is None.
    - Result contains an error.
    - Result has an explicit failure status.
    - Result is empty.
    """
 
    # ---------------------------------------------------------
    # 1. None result
    # ---------------------------------------------------------
    if result is None:
        return {
            "tool": tool_name,
            "passed": False,
            "status": "FAIL",
            "reason": "Tool returned None.",
        }
 
    # ---------------------------------------------------------
    # 2. Dictionary result
    # ---------------------------------------------------------
    if isinstance(result, dict):
 
        # Explicit error returned by tool
        if "error" in result:
            return {
                "tool": tool_name,
                "passed": False,
                "status": "FAIL",
                "reason": str(result["error"]),
            }
 
        # Explicit failure status
        status = result.get("status")
 
        if isinstance(status, str):
            if status.upper() in {
                "FAILED",
                "FAIL",
                "ERROR",
                "FAILURE",
            }:
                return {
                    "tool": tool_name,
                    "passed": False,
                    "status": "FAIL",
                    "reason": (
                        f"Tool returned status {status}."
                    ),
                }
 
        # Empty dictionary
        if not result:
            return {
                "tool": tool_name,
                "passed": False,
                "status": "FAIL",
                "reason": (
                    "Tool returned an empty result."
                ),
            }
 
        return {
            "tool": tool_name,
            "passed": True,
            "status": "PASS",
            "reason": (
                "Tool returned valid evidence."
            ),
        }
 
    # ---------------------------------------------------------
    # 3. List result
    # ---------------------------------------------------------
    if isinstance(result, list):
 
        if len(result) == 0:
            return {
                "tool": tool_name,
                "passed": False,
                "status": "FAIL",
                "reason": (
                    "Tool returned an empty list."
                ),
            }
 
        return {
            "tool": tool_name,
            "passed": True,
            "status": "PASS",
            "reason": (
                "Tool returned evidence."
            ),
        }
 
    # ---------------------------------------------------------
    # 4. String result
    # ---------------------------------------------------------
    if isinstance(result, str):
 
        if not result.strip():
            return {
                "tool": tool_name,
                "passed": False,
                "status": "FAIL",
                "reason": (
                    "Tool returned an empty string."
                ),
            }
 
        return {
            "tool": tool_name,
            "passed": True,
            "status": "PASS",
            "reason": (
                "Tool returned a non-empty result."
            ),
        }
 
    # ---------------------------------------------------------
    # 5. Other valid result types
    # ---------------------------------------------------------
    return {
        "tool": tool_name,
        "passed": True,
        "status": "PASS",
        "reason": (
            "Tool returned a valid result."
        ),
    }
 
 
class Week4Evaluator:
    """
    Evaluates deterministic triage and replay behavior.
 
    Checks:
 
    1. Recommendation generation
    2. Safety behavior
    3. Replay behavior
    4. Tool result evaluation
    """
 
    def __init__(self):
        self.recommender = AgentRecommender()
        self.safety_checker = SafetyChecker()
 
    # =========================================================
    # Recommendation Evaluation
    # =========================================================
 
    def evaluate_recommendation(
        self,
        alarm: str,
        telemetry: dict[str, Any],
        expected_recommendation: str,
    ) -> dict[str, Any]:
 
        recommendation = self.recommender.recommend(
            alarm=alarm,
            telemetry=telemetry,
            maintenance_history=[],
            spare_inventory=[],
            rag_evidence=[],
        )
 
        passed = (
            recommendation == expected_recommendation
        )
 
        return {
            "test": "recommendation",
            "passed": passed,
            "actual": recommendation,
            "expected": expected_recommendation,
        }
 
    # =========================================================
    # Safety Evaluation
    # =========================================================
 
    def evaluate_safety(
        self,
        telemetry: dict[str, Any],
        expected_passed: bool,
    ) -> dict[str, Any]:
 
        result = self.safety_checker.check(
            telemetry=telemetry,
            severity="HIGH",
        )
 
        if isinstance(result, dict):
 
            actual_passed = result.get(
                "passed",
                False,
            )
 
        elif isinstance(result, bool):
 
            actual_passed = result
 
        else:
 
            actual_passed = True
 
        return {
            "test": "safety",
            "passed": (
                actual_passed == expected_passed
            ),
            "actual": actual_passed,
            "expected": expected_passed,
            "details": result,
        }
 
    # =========================================================
    # Replay Evaluation
    # =========================================================
 
    def evaluate_replay(
        self,
        alarm: str,
        original_telemetry: dict[str, Any],
        replay_telemetry: dict[str, Any],
        expected_changed: bool,
    ) -> dict[str, Any]:
 
        original = self.recommender.recommend(
            alarm=alarm,
            telemetry=original_telemetry,
            maintenance_history=[],
            spare_inventory=[],
            rag_evidence=[],
        )
 
        replayed = self.recommender.recommend(
            alarm=alarm,
            telemetry=replay_telemetry,
            maintenance_history=[],
            spare_inventory=[],
            rag_evidence=[],
        )
 
        changed = original != replayed
 
        return {
            "test": "replay",
            "passed": (
                changed == expected_changed
            ),
            "actual_changed": changed,
            "expected_changed": expected_changed,
            "original_recommendation": original,
            "replayed_recommendation": replayed,
        }
 
    # =========================================================
    # Tool Evaluation
    # =========================================================
 
    def evaluate_tool(
        self,
        tool_name: str,
        result: Any,
    ) -> dict[str, Any]:
 
        return evaluate_tool_result(
            tool_name=tool_name,
            result=result,
        )
 
    # =========================================================
    # Complete Evaluation
    # =========================================================
 
    def run_evaluation(
        self,
    ) -> dict[str, Any]:
 
        results = []
 
        # -----------------------------------------------------
        # Test 1 - Normal temperature
        # -----------------------------------------------------
        results.append(
            self.evaluate_recommendation(
                alarm="High temperature alarm",
                telemetry={
                    "temperature": 80
                },
                expected_recommendation=(
                    "Inspect the temperature sensor "
                    "and cooling system."
                ),
            )
        )
 
        # -----------------------------------------------------
        # Test 2 - High temperature
        # -----------------------------------------------------
        results.append(
            self.evaluate_recommendation(
                alarm="High temperature alarm",
                telemetry={
                    "temperature": 95
                },
                expected_recommendation=(
                    "Inspect the cooling system, "
                    "cooling fan and temperature sensor."
                ),
            )
        )
 
        # -----------------------------------------------------
        # Test 3 - Safe telemetry
        # -----------------------------------------------------
        results.append(
            self.evaluate_safety(
                telemetry={
                    "temperature": 80
                },
                expected_passed=True,
            )
        )
 
        # -----------------------------------------------------
        # Test 4 - Critical telemetry
        # -----------------------------------------------------
        results.append(
            self.evaluate_safety(
                telemetry={
                    "temperature": 105
                },
                expected_passed=False,
            )
        )
 
        # -----------------------------------------------------
        # Test 5 - Replay changes recommendation
        # -----------------------------------------------------
        results.append(
            self.evaluate_replay(
                alarm="High temperature alarm",
                original_telemetry={
                    "temperature": 80
                },
                replay_telemetry={
                    "temperature": 95
                },
                expected_changed=True,
            )
        )
 
        # -----------------------------------------------------
        # Summary
        # -----------------------------------------------------
        total = len(results)
 
        passed = sum(
            1
            for result in results
            if result["passed"]
        )
 
        failed = total - passed
 
        score = (
            (passed / total) * 100
            if total > 0
            else 0
        )
 
        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "score_percent": score,
            "results": results,
        }