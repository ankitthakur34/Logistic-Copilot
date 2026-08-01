from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.langgraph.state import AgentState

from app.langgraph.nodes.router_node import RouterNode
from app.langgraph.nodes.sql_node import SQLNode
from app.langgraph.nodes.rag_node import RAGNode
from app.langgraph.nodes.coordinator_node import CoordinatorNode
from app.langgraph.nodes.merger_node import MergeNode
from app.agents.router_agent.router_decision import RouterDecision


class LogisticsCopilotGraph:

    def __init__(

        self,

        router_llm,

        sql_tool,

        rag_tool,

        answer_merger,

    ):

        ####################################################
        # Graph Builder
        ####################################################

        builder = StateGraph(

            AgentState,

        )

        ####################################################
        # Nodes
        ####################################################

        builder.add_node(

            "router",

            RouterNode(

                router_llm,

            ),

        )

        builder.add_node(

            "sql",

            SQLNode(

                sql_tool,

            ),

        )

        builder.add_node(

            "rag",

            RAGNode(

                rag_tool,

            ),

        )

        builder.add_node(

            "coordinator",

            CoordinatorNode(),

        )

        builder.add_node(

            "merge",

            MergeNode(

                answer_merger,

            ),

        )

        builder.add_edge(START, "router")

        builder.add_edge("router", "sql")
        builder.add_edge("router", "rag")

        builder.add_edge("sql", "coordinator")
        builder.add_edge("rag", "coordinator")

        builder.add_edge("coordinator", "merge")

        builder.add_edge("merge", END)

        ####################################################
        # Compile
        ####################################################

        self.graph = builder.compile()



   

    ####################################################
    # Invoke
    ####################################################

    def invoke(

        self,

        state: AgentState,

    ):

        return self.graph.invoke(

            state,

        )