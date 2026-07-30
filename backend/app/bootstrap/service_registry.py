from app.bootstrap.rag import build_rag
from app.bootstrap.sql import build_sql

from app.tools.rag_tool import RAGTool
from app.tools.sql_tool import SQLTool


class ServiceRegistry:

    def __init__(self):

        ###################################################
        # SQL
        ###################################################

        sql = build_sql()

        self.sql_agent = sql.agent

        self.sql_tool = SQLTool(

            agent=self.sql_agent

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