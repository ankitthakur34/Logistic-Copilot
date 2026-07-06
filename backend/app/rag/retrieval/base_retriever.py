from abc import ABC, abstractmethod


class BaseRetriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query_embedding,
        question,
        top_k: int = 5,
    ):
        pass