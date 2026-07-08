from abc import ABC, abstractmethod

from app.rag.schema.retrieval_result import RetrievalResult
from app.rag.prompts.prompt_result import PromptResult


class BasePromptBuilder(ABC):

    @abstractmethod
    def build(
        self,
        question: str,
        retrieval: RetrievalResult,
    ) -> PromptResult:
        pass