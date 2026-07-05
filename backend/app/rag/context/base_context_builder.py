from abc import ABC, abstractmethod

from app.rag.schema.retrieval_result import RetrievalResult
from app.rag.context.context_result import ContextResult


class BaseContextBuilder(ABC):

    @abstractmethod
    def build(
        self,
        retrieval: RetrievalResult,
    ) -> ContextResult:
        pass