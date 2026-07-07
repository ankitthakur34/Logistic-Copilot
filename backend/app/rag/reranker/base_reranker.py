from abc import ABC, abstractmethod


class BaseReranker(ABC):

    @abstractmethod
    def rerank(
        self,
        question: str,
        children,
        top_k: int = 5,
    ):
        pass