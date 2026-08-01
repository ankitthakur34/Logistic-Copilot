from app.langgraph.state import AgentState
from app.agents.router_agent.router_decision import RouterDecision


class RAGNode:

    def __init__(

        self,

        rag_tool,

    ):

        self.rag_tool = rag_tool

    ####################################################
    # Execute
    ####################################################

    def __call__(

        self,

        state: AgentState,

    ):

        ################################################
        # Check whether RAG is selected
        ################################################

        if RouterDecision.RAG not in state["router_result"].tools:

            return {}

        ################################################
        # Execute RAG
        ################################################

        result = self.rag_tool.execute(

            question=state["question"],

        )

        ################################################
        # Return partial state
        ################################################

        return {

            "tool_results": {

                self.rag_tool.name: result,

            }

        }