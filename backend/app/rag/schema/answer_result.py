from dataclasses import dataclass

from app.rag.llm.llm_result import LLMResult
from app.rag.schema.retrieval_result import RetrievalResult


@dataclass
class AnswerResult:

    answer: str

    retrieval: RetrievalResult

    llm_result: LLMResult