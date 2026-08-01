from app.langgraph.state import AgentState
from app.agents.router_agent.router_decision import RouterDecision


class SQLNode:

    def __init__(

        self,

        sql_tool,

    ):

        self.sql_tool = sql_tool

    ####################################################
    # Execute
    ####################################################

    def __call__(

        self,

        state: AgentState,

    ):

        ################################################
        # Check whether SQL is selected
        ################################################

        if RouterDecision.SQL not in state["router_result"].tools:

            return {}

        ################################################
        # Execute SQL
        ################################################

        result = self.sql_tool.execute(

            question=state["question"],

        )

        ################################################
        # Return partial state
        ################################################

        return {

            "tool_results": {

                self.sql_tool.name: result,

            }

        }