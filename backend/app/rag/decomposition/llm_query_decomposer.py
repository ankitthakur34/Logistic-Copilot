import json

from app.rag.prompts.prompt_result import (
    PromptResult,
)

from app.rag.decomposition.base_query_decomposer import (
    BaseQueryDecomposer,
)

from app.rag.decomposition.prompts.query_decomposition_prompt import (
    SYSTEM_PROMPT,
)

from app.rag.utils.json_parser import (
    JsonParser,
)


class LLMQueryDecomposer(
    BaseQueryDecomposer
):

    def __init__(
        self,
        llm,
    ):
        self.llm = llm

    def decompose(
        self,
        question: str,
    ) -> list[str]:

        prompt = PromptResult(

            system_prompt=SYSTEM_PROMPT,

            user_prompt=question,

            full_prompt="",

        )

        response = self.llm.generate(
            prompt,
        )

        try:

            data = JsonParser.parse(
                response.answer,
            )

            queries = data.get(
                "queries",
                [],
            )

        except Exception:

            return [
                question
            ]

        if not queries:

            return [
                question
            ]

        return queries