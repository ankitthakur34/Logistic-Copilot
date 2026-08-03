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
        # Extract shipment number
        ###################################################

        shipment_match = re.search(

            r"\b(SHP\d+)\b",

            question,

        )

        state["shipment_no"] = (

            shipment_match.group(1)

            if shipment_match

            else None

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