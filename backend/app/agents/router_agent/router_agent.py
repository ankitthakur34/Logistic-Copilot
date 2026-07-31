from app.agents.router_agent.router_llm import (
    RouterLLM,
)

from app.agents.router_agent.router_parser import (
    RouterParser,
)

from app.agents.router_agent.router_answer_merger import (
    RouterAnswerMerger,
)



from app.tools.base_tool import (
    BaseTool,
)

from app.tools.tool_result import (
    ToolResult,
)
from app.agents.router_agent.router_execution_result import RouterExecutionResult


class RouterAgent:

    def __init__(

        self,

        router_llm: RouterLLM,

        answer_merger: RouterAnswerMerger,

        tools: dict[str, BaseTool],

    ):

        self.router_llm = router_llm

        self.answer_merger = answer_merger

        self.tools = tools

    #################################################
    # Run
    #################################################

    def run(

        self,

        question: str,

    ) -> RouterExecutionResult:

        #################################################
        # Router
        #################################################

        response = self.router_llm.route(

            question

        )

        #################################################
        # Parse
        #################################################

        router_result = RouterParser.parse(

            response

        )

        print()

        print("=" * 80)
        print("ROUTER RESULT")
        print(router_result)

        #################################################
        # No Tool Selected
        #################################################

        if not router_result.tools:

            failed_result = ToolResult(

                tool_name="router",

                success=False,

                answer="",

                error=router_result.reason,

                metadata={

                    "router_confidence": router_result.confidence,

                },

            )

            return RouterExecutionResult(

                answer="I couldn't determine which tool should answer this question.",

                tool_results=[

                    failed_result,

                ],

            )

        #################################################
        # Execute Selected Tools
        #################################################

        tool_results = []

        for decision in router_result.tools:

            tool = self.tools.get(

                decision.value,

            )

            if tool is None:

                tool_results.append(

                    ToolResult(

                        tool_name=decision.value,

                        success=False,

                        answer="",

                        error=f"{decision.value} tool not registered.",

                    )

                )

                continue

            result = tool.execute(

                question=question,

            )

            result.metadata = result.metadata or {}

            result.metadata.update(

                {

                    "router_confidence": router_result.confidence,

                    "router_reason": router_result.reason,

                }

            )

            tool_results.append(

                result,

            )

        #################################################
        # Merge Answers
        #################################################

        final_answer = self.answer_merger.merge(

            question=question,

            results=tool_results,

        )

        #################################################

        return RouterExecutionResult(

            answer=final_answer,

            tool_results=tool_results,

        )