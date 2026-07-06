from app.rag.schema.document import ParentChunk
from app.rag.schema.retrieval_result import (
    RetrievalResult,
    RetrievedChild,
)


class RetrievalPipeline:

    def __init__(
        self,
        embedding_model,
        retriever,
    ):

        self.embedding_model = embedding_model
        self.retriever = retriever

    def run(
        self,
        question: str,
        ingestion,
        top_k: int = 5,
    ):

        query_embedding = self.embedding_model.embed_query(
            question
        )

        search_result = self.retriever.retrieve(
            query_embedding=query_embedding,
            question=question,
            top_k=top_k,
        )

        children = []

        parents = {}

        for idx,child_id in enumerate(search_result.ids):
               

            child_chunk = ingestion.child_lookup[child_id]

            child = RetrievedChild(

        id=child_chunk.id,

        parent_id=child_chunk.parent_id,

        content=child_chunk.content,

        metadata=child_chunk.metadata,

        score=search_result.scores[idx],

    )

            children.append(child)

            parent = ingestion.parent_lookup[
                child.parent_id
            ]

            parents[parent.id] = parent

        return RetrievalResult(

            children=children,

            parents=list(parents.values()),

        )