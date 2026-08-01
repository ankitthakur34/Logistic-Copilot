from app import create_app

from app.bootstrap.service_registry import (
    ServiceRegistry,
)

from app.langgraph.state import (
    AgentState,
)
from app.debug.state_formatter import StateFormatter


app = create_app()

with app.app_context():

    registry = ServiceRegistry()

    state: AgentState = {

        "question": "What is customer clearnce SOP?",

        "router_result": None,

        "tool_results": {},

        "all_tools_success": False,

        "answer": None,

        "execution_result": None,

    }

    result = registry.graph.invoke(

        state,

    )

    StateFormatter.print(result)