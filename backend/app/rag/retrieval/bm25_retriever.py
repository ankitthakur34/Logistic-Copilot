from app.rag.retrieval.base_retriever import BaseRetriever
from app.rag.schema.search_result import SearchResult


class BM25Retriever(BaseRetriever):

    def __init__(
        self,
        bm25_index,
    ):
        self.bm25_index = bm25_index

    def retrieve(
        self,
        query_embedding=None,
        question=None,
        where=None,
        top_k=5,
    ) -> SearchResult:

        result = self.bm25_index.search(
            query=question,
            top_k=len(self.bm25_index.child_chunks),
        )

        if not where:
            result.ids = result.ids[:top_k]
            result.scores = result.scores[:top_k]
            return result

        filtered_ids = []
        filtered_scores = []

        for chunk_id, score in zip(
            result.ids,
            result.scores,
        ):

            child = self.bm25_index.child_chunks_by_id[
                chunk_id
            ]

            matched = True

            for key, value in where.items():

                if child.metadata.get(key) != value:
                    matched = False
                    break

            if matched:

                filtered_ids.append(chunk_id)
                filtered_scores.append(score)

            if len(filtered_ids) >= top_k:
                break

        return SearchResult(
            ids=filtered_ids,
            scores=filtered_scores,
        )