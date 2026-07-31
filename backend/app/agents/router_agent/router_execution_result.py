from dataclasses import dataclass

from app.tools.tool_result import ToolResult


@dataclass
class RouterExecutionResult:

    answer: str

    tool_results: list[ToolResult]