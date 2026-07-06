from collections import defaultdict

from app.rag.schema.search_result import SearchResult


class ReciprocalRankFusion:

    def __init__(
        self,
        k: int = 60,
    ):
        self.k = k

    def fuse(
        self,
        results: list[SearchResult],
        top_k: int = 5,
    ) -> SearchResult:

        fused_scores = defaultdict(float)

        for result in results:

            for rank, doc_id in enumerate(result.ids):

                fused_scores[doc_id] += 1.0 / (
                    self.k + rank + 1
                )

        ranked = sorted(

            fused_scores.items(),

            key=lambda item: item[1],

            reverse=True,

        )[:top_k]

        return SearchResult(

            ids=[doc_id for doc_id, _ in ranked],

            scores=[score for _, score in ranked],

        )