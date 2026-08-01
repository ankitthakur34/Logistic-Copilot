from app.langgraph.state import AgentState
from app.agents.router_agent.router_llm import RouterLLM


class RouterNode:

    def __init__(
        self,
        router_llm: RouterLLM,
    ):
        self.router_llm = router_llm

    ####################################################
    # Execute
    ####################################################

    def __call__(
        self,
        state: AgentState,
    ):

        router_result = self.router_llm.route(

            state["question"]

        )

        return {

            "router_result": router_result,

        }