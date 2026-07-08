from abc import ABC, abstractmethod

from app.rag.schema.retrieval_result import RetrievalResult


class BaseContextCompressor(ABC):

    @abstractmethod
    def compress(
        self,
        retrieval: RetrievalResult,
    ) -> RetrievalResult:
        pass