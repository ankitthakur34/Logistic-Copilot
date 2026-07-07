from app.rag.multi_query.base_multi_query_generator import (
    BaseMultiQueryGenerator,
)

from app.rag.multi_query.parser import (
    MultiQueryParser,
)

from app.rag.multi_query.multi_query_prompt_builder import (
    MultiQueryPromptBuilder,
)


class LLMMultiQueryGenerator(BaseMultiQueryGenerator):

    def __init__(
        self,
        llm,
    ):

        self.llm = llm

        self.prompt_builder = MultiQueryPromptBuilder()

    def generate(
        self,
        question: str,
    ) -> list[str]:

        prompt = self.prompt_builder.build(
            question,
        )

        result = self.llm.generate(
            prompt,
        )

        return MultiQueryParser.parse(
            result.answer,
        )