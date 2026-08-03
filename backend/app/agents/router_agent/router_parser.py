import json
import re

from app.agents.router_agent.router_result import (
    RouterResult,
)

from app.agents.router_agent.router_decision import (
    RouterDecision,
)


class RouterParser:

    @staticmethod
    def parse(

        response: str,

    ) -> RouterResult:

        ##################################################
        # Remove markdown fences
        ##################################################

        response = re.sub(

            r"```json|```",

            "",

            response,

            flags=re.IGNORECASE,

        ).strip()

        ##################################################
        # Parse JSON
        ##################################################

        try:

            data = json.loads(

                response

            )

        except Exception:

            return RouterResult(

                tools=[],

                confidence=0.0,

                reason="Router returned invalid JSON.",

            )

        ##################################################
        # Parse Tools
        ##################################################

        parsed_tools = []

        raw_tools = data.get(

            "tools",

            [],

        )

        if isinstance(

            raw_tools,

            str,

        ):

            raw_tools = [

                raw_tools

            ]

        for tool in raw_tools:

            tool = str(

                tool

            ).lower()

            if tool == "sql":

                parsed_tools.append(

                    RouterDecision.SQL

                )

            elif tool == "rag":

                parsed_tools.append(

                    RouterDecision.RAG

                )
            elif tool == "ml":

                parsed_tools.append(

            RouterDecision.ML

        )    

        ##################################################
        # Confidence
        ##################################################

        confidence = float(

            data.get(

                "confidence",

                0.0,

            )

        )

        confidence = max(

            0.0,

            min(

                confidence,

                1.0,

            ),

        )

        ##################################################
        # Reason
        ##################################################

        reason = str(

            data.get(

                "reason",

                "",

            )

        )

        ##################################################

        return RouterResult(

            tools=parsed_tools,

            confidence=confidence,

            reason=reason,

        )