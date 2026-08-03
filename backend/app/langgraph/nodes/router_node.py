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
        print("=" * 50)
        print("ROUTER")
        print(router_result.tools)
        print("=" * 50)

        return {

            "router_result": router_result,

        }