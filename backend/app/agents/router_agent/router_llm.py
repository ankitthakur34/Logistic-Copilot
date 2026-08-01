from app.rag.prompts.prompt_result import PromptResult
from app.rag.llm.base_llm import BaseLLM

from app.agents.router_agent.router_prompt import (
    ROUTER_SYSTEM_PROMPT,
)

from app.agents.router_agent.router_parser import (
    RouterParser,
)

from app.agents.router_agent.router_result import (
    RouterResult,
)


class RouterLLM:

    def __init__(

        self,

        llm: BaseLLM,

    ):

        self.llm = llm

        self.parser = RouterParser()

    ####################################################
    # Route
    ####################################################

    def route(

        self,

        question: str,

    ) -> RouterResult:

        user_prompt = f"""
QUESTION:

{question}

Return ONLY valid JSON.
"""

        prompt = PromptResult(

            system_prompt=ROUTER_SYSTEM_PROMPT,

            user_prompt=user_prompt,

            full_prompt="",

        )

        response = self.llm.generate(

            prompt,

        )

        return self.parser.parse(

            response.answer,

        )