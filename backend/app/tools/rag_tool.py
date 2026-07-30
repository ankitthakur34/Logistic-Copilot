from app.tools.base_tool import BaseTool
from app.tools.tool_result import ToolResult

from app.rag.answer_pipeline import AnswerPipeline


class RAGTool(BaseTool):

    def __init__(

        self,

        pipeline: AnswerPipeline,

        ingestion,

    ):

        self.pipeline = pipeline

        self.ingestion = ingestion

    @property
    def name(self):

        return "rag"

    @property
    def description(self):

        return (

            "Use this tool for searching unstructured "

            "documents like SOPs, emails, PDFs, markdown "

            "documents, incidents and manuals."

        )

    def execute(

        self,

        **kwargs,

    ) -> ToolResult:

        question = kwargs.get(

            "question"

        )

        if not question:

            return ToolResult(

                tool_name=self.name,

                success=False,

                answer="",

                error="Question is required.",

            )

        try:

            result = self.pipeline.run(

                question=question,

                ingestion=self.ingestion,

                top_k=5,

            )

            return ToolResult(

                tool_name=self.name,

                success=True,

                answer=result.answer,

                metadata={

                    "question": question,

                    "sources":[

                        p.metadata.get("source")

                        for p in result.retrieval.parents

                    ],

                    "parent_count":len(

                        result.retrieval.parents

                    ),

                    "child_count":len(

                        result.retrieval.children

                    ),

                    "llm_model":result.llm_result.model,

                    "token_usage":result.llm_result.usage,

                },

                data=result.retrieval,

            )

        except Exception as e:

            return ToolResult(

                tool_name=self.name,

                success=False,

                answer="",

                error=str(e),

            )