import re

from app.langgraph.state import AgentState


class NormalizerNode:

    def __call__(

        self,

        state: AgentState,

    ) -> AgentState:

        question = state["question"].strip()

        ###################################################
        # Normalize shipment ids
        ###################################################

        question = re.sub(

            r"\bshp\d+\b",

            lambda m: m.group().upper(),

            question,

            flags=re.IGNORECASE,

        )

        ###################################################
        # Normalize container ids (future)
        ###################################################

        question = re.sub(

            r"\bcont\d+\b",

            lambda m: m.group().upper(),

            question,

            flags=re.IGNORECASE,

        )

        ###################################################
        # Collapse multiple spaces
        ###################################################

        question = " ".join(question.split())

        state["question"] = question

        return state