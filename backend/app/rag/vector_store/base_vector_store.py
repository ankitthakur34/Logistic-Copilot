from abc import ABC, abstractmethod

from app.rag.schema.document import ChildChunk
from app.rag.schema.search_result import SearchResult


class BaseVectorStore(ABC):

    @abstractmethod
    def index(
        self,
        child_chunks: list[ChildChunk],
        embeddings: list[list[float]],
    ):
        """
        Store child chunks and their embeddings
        inside the vector database.
        """
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> SearchResult:
        """
        Search the vector database.
        """
        pass