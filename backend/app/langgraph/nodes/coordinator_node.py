from app.langgraph.state import AgentState


class CoordinatorNode:

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

        tool_results = state.get(

            "tool_results",

            {},

        )

        ################################################
        # Success
        ################################################

        all_success = all(

            result.success

            for result in tool_results.values()

        )

        ################################################
        # Return partial state
        ################################################

        return {

            "all_tools_success": all_success,

        }