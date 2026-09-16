from typing import Any, Callable
 
from app.schemas.case_state import CaseState
from app.services.tool_executor import (
    ToolExecutionError,
    ToolExecutor,
)
 
 
class SafeToolRunner:
    """
    Executes tools safely and records failures
    in the current case state.
    """
 
    def __init__(
        self,
        executor: ToolExecutor | None = None,
    ):
        self.executor = executor or ToolExecutor()
 
    def run(
        self,
        case: CaseState,
        tool_name: str,
        tool: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any | None:
        """
        Execute a tool.
 
        If the tool fails after retries, record the
        failure in CaseState instead of crashing
        the complete workflow.
        """
 
        try:
            result = self.executor.execute(
                tool,
                *args,
                **kwargs,
            )
 
            if tool_name not in case.completed_steps:
                case.completed_steps.append(tool_name)
 
            return result
 
        except ToolExecutionError as exc:
 
            error_message = (
                f"{tool_name} tool failed: {exc}"
            )
 
            case.errors.append(error_message)
 
            return None