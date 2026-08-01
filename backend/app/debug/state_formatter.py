from app.langgraph.state import AgentState


class StateFormatter:

    @staticmethod
    def print(state: AgentState):

        print()

        print("=" * 80)
        print("QUESTION")
        print("=" * 80)

        print(state["question"])

        print()

        print("=" * 80)
        print("ROUTER")
        print("=" * 80)

        router = state["router_result"]

        print(
            "Tools      :",
            ", ".join(
                tool.value.upper()
                for tool in router.tools
            ),
        )

        print(
            "Confidence :",
            router.confidence,
        )

        print(
            "Reason     :",
            router.reason,
        )

        print()

        print("=" * 80)
        print("TOOLS")
        print("=" * 80)

        for result in state["execution_result"].tool_results:

            print()

            print(result.tool_name.upper())

            print("-" * 40)

            print(
                "Success :",
                result.success,
            )

            print(
                "Answer  :",
                result.answer,
            )

            metadata = result.metadata or {}

            sources = metadata.get(
                "sources",
                [],
            )

            if sources:

                print()

                print("Sources")

                for source in sources:

                    print(
                        f" • {source}"
                    )

        print()

        print("=" * 80)
        print("FINAL ANSWER")
        print("=" * 80)

        print(
            state["answer"],
        )

        print()