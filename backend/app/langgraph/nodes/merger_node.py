from app.langgraph.state import AgentState

from app.agents.router_agent.router_execution_result import (
    RouterExecutionResult,
)

from app.agents.router_agent.router_answer_merger import (
    RouterAnswerMerger,
)


class MergeNode:

    def __init__(

        self,

        answer_merger: RouterAnswerMerger,

    ):

        self.answer_merger = answer_merger

    ####################################################
    # Execute
    ####################################################

    def __call__(

        self,

        state: AgentState,

    ):

        ################################################
        # Tool Results
        ################################################

        results = list(

            state.get(

                "tool_results",

                {},

            ).values()

        )

        ################################################
        # Merge Answers
        ################################################

        answer = self.answer_merger.merge(

            question=state["question"],

            results=results,

        )

        ################################################
        # Build Execution Result
        ################################################

        execution_result = RouterExecutionResult(

            answer=answer,

            tool_results=results,

        )

        ################################################
        # Return partial state
        ################################################

        return {

            "answer": answer,

            "execution_result": execution_result,

        }