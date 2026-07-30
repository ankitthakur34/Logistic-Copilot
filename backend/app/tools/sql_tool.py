from app.tools.base_tool import (
    BaseTool,
)

from app.tools.tool_result import (
    ToolResult,
)
from app.agents.sql_agent.sql_agent import SQLAgent




class SQLTool(BaseTool):

    def __init__(

        self,

        agent: SQLAgent,

    ):

        self.agent = agent

    #################################################
    # Tool Name
    #################################################

    @property
    def name(self) -> str:

        return "sql"

    #################################################
    # Description
    #################################################

    @property
    def description(self) -> str:

        return (
            "Use this tool to answer structured database questions "
            "about shipments, containers, vessels, ports, users, "
            "tasks, statistics and reports."
        )

    #################################################
    # Execute
    #################################################

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

            result = self.agent.run(

                question

            )

            return ToolResult(

                tool_name=self.name,

                success=True,

                answer=result.answer,

                data=result.rows,

                metadata={

                    "question": result.question,

                    "generated_sql": getattr(
                        result,
                        "generated_sql",
                        result.sql,
                    ),

                    "normalized_sql": getattr(
                        result,
                        "normalized_sql",
                        result.sql,
                    ),

                },

            )

        except Exception as e:

            return ToolResult(

                tool_name=self.name,

                success=False,

                answer="",

                error=str(e),

            )