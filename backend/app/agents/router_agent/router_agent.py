from app.langgraph.state import AgentState


class RouterAgent:

    def __init__(

        self,

        graph,

    ):

        self.graph = graph

    ####################################################
    # Run
    ####################################################

    def run(

        self,

        question: str,

    ):

        state: AgentState = {

            "question": question,

            "router_result": None,

            "tool_results": {},

            "all_tools_success": False,

            "answer": None,

            "execution_result": None,

        }

        final_state = self.graph.invoke(

            state,

        )

        return final_state[

            "execution_result"

        ]