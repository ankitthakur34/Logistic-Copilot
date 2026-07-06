from app.rag.retrieval.base_retriever import BaseRetriever
from app.rag.retrieval.rrf import ReciprocalRankFusion


class HybridRetriever(BaseRetriever):

    def __init__(
        self,
        dense_retriever: BaseRetriever,
        sparse_retriever: BaseRetriever,
        fusion: ReciprocalRankFusion | None = None,
    ):

        self.dense_retriever = dense_retriever
        self.sparse_retriever = sparse_retriever
        self.fusion = fusion or ReciprocalRankFusion()

    def retrieve(
        self,
        query_embedding,
        question,
        top_k: int = 10,
    ):

        dense_result = self.dense_retriever.retrieve(

            query_embedding=query_embedding,

            question=question,

            top_k=top_k,

        )

        sparse_result = self.sparse_retriever.retrieve(

            query_embedding=query_embedding,

            question=question,

            top_k=top_k,

        )

        return self.fusion.fuse(

            [dense_result, sparse_result],

            top_k=top_k,

        )