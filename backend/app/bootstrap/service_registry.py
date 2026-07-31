from app.bootstrap.rag import (
    build_rag,
)

from app.bootstrap.sql import (
    build_sql,
)

from app.bootstrap.llm import (
    get_llm,
)

from app.tools.rag_tool import (
    RAGTool,
)

from app.tools.sql_tool import (
    SQLTool,
)

from app.agents.router_agent.router_agent import (
    RouterAgent,
)
from app.agents.router_agent.router_answer_merger import (
    RouterAnswerMerger,
)

from app.agents.router_agent.router_llm import (
    RouterLLM,
)
from app.tools.base_tool import BaseTool


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

        ###################################################
        # TOOL REGISTRY
        ###################################################

        self.tools = {}

        self.register_tool(

            self.sql_tool,

        )

        self.register_tool(

            self.rag_tool,

        )

        ###################################################
        # ROUTER
        ###################################################

        self.router_agent = RouterAgent(

    router_llm=RouterLLM(

        get_llm(),

    ),

    answer_merger=RouterAnswerMerger(

        get_llm(),

    ),

    tools=self.tools,

)

    ###################################################
    # Register Tool
    ###################################################

    def register_tool(

        self,

        tool: BaseTool,

    ):

        self.tools[tool.name] = tool