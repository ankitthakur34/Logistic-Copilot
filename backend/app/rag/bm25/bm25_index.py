from rank_bm25 import BM25Okapi

from app.rag.bm25.tokenizer import Tokenizer
from app.rag.schema.document import ChildChunk
from app.rag.schema.search_result import SearchResult


class BM25Index:

    def __init__(self):

        self.bm25 = None

        self.child_chunks: list[ChildChunk] = []

    def build(
    self,
    child_chunks,
):

        self.child_chunks = child_chunks

        self.child_chunks_by_id = {
        chunk.id: chunk
        for chunk in child_chunks
    }

        corpus = [
        Tokenizer.tokenize(chunk.content)
        for chunk in child_chunks
    ]

        self.bm25 = BM25Okapi(corpus)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> SearchResult:

        if self.bm25 is None:

            raise RuntimeError(
                "BM25 index has not been built."
            )

        tokens = Tokenizer.tokenize(query)

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(

            enumerate(scores),

            key=lambda x: x[1],

            reverse=True,

        )[:top_k]

        ids = []
        retrieved_scores = []

        for index, score in ranked:

            ids.append(
                self.child_chunks[index].id
            )

            retrieved_scores.append(
                float(score)
            )

        return SearchResult(

            ids=ids,

            scores=retrieved_scores,

        )