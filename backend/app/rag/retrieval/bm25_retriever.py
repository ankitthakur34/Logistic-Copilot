from app.rag.retrieval.base_retriever import BaseRetriever
from app.rag.bm25.bm25_index import BM25Index
from app.rag.schema.search_result import SearchResult


class BM25Retriever(BaseRetriever):

    def __init__(
        self,
        bm25_index: BM25Index,
    ):
        self.bm25_index = bm25_index

    def retrieve(
        self,
        query_embedding=None,
        question: str = None,
        top_k: int = 20,
    ) -> SearchResult:

        return self.bm25_index.search(
            query=question,
            top_k=top_k,
        )