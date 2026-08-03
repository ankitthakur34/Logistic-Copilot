from app.bootstrap.rag import build_rag
from app.bootstrap.sql import build_sql
from app.bootstrap.llm import get_llm

from app.tools.rag_tool import RAGTool
from app.tools.sql_tool import SQLTool
from app.tools.base_tool import BaseTool

from app.agents.router_agent.router_agent import RouterAgent
from app.agents.router_agent.router_answer_merger import RouterAnswerMerger
from app.agents.router_agent.router_llm import RouterLLM

from app.langgraph.graph import LogisticsCopilotGraph
from app.tools.ml_tool import MLTool


class ServiceRegistry:

    def __init__(self):

        ###################################################
        # SQL
        ###################################################

        sql = build_sql()

        self.sql_agent = sql.agent

        self.sql_tool = SQLTool(

            agent=self.sql_agent,

        )

        ###################################################
        # RAG
        ###################################################

        rag = build_rag()

        self.rag_pipeline = rag.pipeline

        self.ingestion = rag.ingestion

        self.rag_tool = RAGTool(

            pipeline=self.rag_pipeline,

            ingestion=self.ingestion,

        )

        self.ml_tool = MLTool()

        ###################################################
        # Tool Registry
        ###################################################

        self.tools = {}

        self.register_tool(self.sql_tool)
        self.register_tool(self.rag_tool)
        self.register_tool(self.ml_tool)

        ###################################################
        # Shared Components
        ###################################################

        self.router_llm = RouterLLM(

            get_llm(),

        )

        self.answer_merger = RouterAnswerMerger(

            get_llm(),

        )

        ###################################################
        # LangGraph
        ###################################################

        self.graph = LogisticsCopilotGraph(

    router_llm=self.router_llm,

    sql_tool=self.sql_tool,

    rag_tool=self.rag_tool,

    ml_tool=self.ml_tool,

    answer_merger=self.answer_merger,

)

        ###################################################
        # Router Agent
        ###################################################

        self.router_agent = RouterAgent(

            graph=self.graph,

        )

    ###################################################
    # Register Tool
    ###################################################

    def register_tool(

        self,

        tool: BaseTool,

    ):

        self.tools[tool.name] = tool