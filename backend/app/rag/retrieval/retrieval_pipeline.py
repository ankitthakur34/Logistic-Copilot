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
            top_k=top_k,
        )

        children = []

        parents = {}

        for idx in range(len(search_result.ids)):

            metadata = search_result.metadatas[idx]

            child = RetrievedChild(

                id=search_result.ids[idx],

                parent_id=metadata["parent_id"],

                content=search_result.documents[idx],

                metadata=metadata,

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