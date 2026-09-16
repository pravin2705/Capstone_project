from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Any, Callable
 
 
class ToolExecutionError(Exception):
    """Raised when a tool cannot be executed successfully."""
 
 
class ToolExecutor:
    """
    Executes tools with retry and timeout handling.
    """
 
    def __init__(
        self,
        max_retries: int = 2,
        timeout_seconds: float = 5.0,
    ):
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
 
    def execute(
        self,
        tool: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Execute a tool with timeout and retry handling.
        """
 
        last_error: Exception | None = None
 
        for attempt in range(self.max_retries + 1):
 
            try:
                with ThreadPoolExecutor(
                    max_workers=1
                ) as executor:
 
                    future = executor.submit(
                        tool,
                        *args,
                        **kwargs,
                    )
 
                    return future.result(
                        timeout=self.timeout_seconds
                    )
 
            except TimeoutError as exc:
 
                last_error = exc
 
            except Exception as exc:
 
                last_error = exc
 
            if attempt < self.max_retries:
                continue
 
        raise ToolExecutionError(
            f"Tool failed after "
            f"{self.max_retries + 1} attempts"
        ) from last_error