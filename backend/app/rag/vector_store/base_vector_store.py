from abc import ABC, abstractmethod

from app.rag.schema.embedding_result import EmbeddingResult


class BaseVectorStore(ABC):

    @property
    @abstractmethod
    def collection_name(self) -> str:
        pass

    @abstractmethod
    def index(
        self,
        embedding_result: EmbeddingResult,
    ):
        pass

    @abstractmethod
    def similarity_search(
        self,
        query_embedding: list[float],
        k: int = 5,
    ):
        pass

    @abstractmethod
    def delete_collection(self):
        pass

    @abstractmethod
    def reset(self):
        pass