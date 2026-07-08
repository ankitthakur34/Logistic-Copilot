from app.rag.llm.base_llm import BaseLLM
from app.rag.prompts.base_prompt_builder import BasePromptBuilder
from app.rag.schema.answer_result import AnswerResult
from app.rag.schema.retrieval_result import RetrievalResult


class AnswerGenerator:

    def __init__(
        self,
        prompt_builder: BasePromptBuilder,
        llm: BaseLLM,
    ):

        self.prompt_builder = prompt_builder
        self.llm = llm

    def generate(
        self,
        question: str,
        retrieval: RetrievalResult,
    ) -> AnswerResult:

        prompt = self.prompt_builder.build(
            question=question,
            retrieval=retrieval,
        )

        llm_result = self.llm.generate(
            prompt,
        )

        return AnswerResult(

            answer=llm_result.answer,

            retrieval=retrieval,

            llm_result=llm_result,

        )