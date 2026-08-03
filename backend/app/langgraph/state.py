from typing import TypedDict
from typing import Annotated
from operator import or_

from app.agents.router_agent.router_result import RouterResult
from app.agents.router_agent.router_execution_result import RouterExecutionResult
from app.tools.tool_result import ToolResult


class AgentState(TypedDict):

    question: str

    shipment_no: str | None

    router_result: RouterResult | None

    tool_results: Annotated[
        dict[str, ToolResult],
        or_,
    ]

    all_tools_success: bool

    answer: str | None

    execution_result: RouterExecutionResult | None