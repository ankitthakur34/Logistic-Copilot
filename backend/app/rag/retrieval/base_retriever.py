from abc import ABC, abstractmethod


class BaseRetriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query_embedding,
        top_k: int = 5,
    ):
        pass