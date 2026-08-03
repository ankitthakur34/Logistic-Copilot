from app.langgraph.state import AgentState
from app.agents.router_agent.router_decision import RouterDecision


class MLNode:

    def __init__(

        self,

        ml_tool,

    ):

        self.ml_tool = ml_tool

    ####################################################
    # Execute
    ####################################################

    def __call__(

        self,

        state: AgentState,

    ):

        if RouterDecision.ML not in state["router_result"].tools:

            return {}

        result = self.ml_tool.execute(

            shipment_no=state["shipment_no"],

        )

        return {

            "tool_results": {

                self.ml_tool.name: result,

            }

        }