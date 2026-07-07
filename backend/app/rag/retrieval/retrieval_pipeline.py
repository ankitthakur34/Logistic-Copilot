
from app.rag.schema.retrieval_result import (
    RetrievalResult,
    RetrievedChild,
)
from app.rag.metadata.regex_metadata_extractor import (
    RegexMetadataExtractor,
)

from app.rag.metadata.metadata_filter import (
    MetadataFilter,
)


class RetrievalPipeline:

    def __init__(
        self,
        embedding_model,
        retriever,
        reranker=None,
        metadata_extractor= None,
    ):

        self.embedding_model = embedding_model
        self.retriever = retriever
        self.reranker = reranker
        self.metadata_extractor = (metadata_extractor or RegexMetadataExtractor()

)

    def run(
        self,
        question: str,
        ingestion,
        top_k: int = 5,
    ) -> RetrievalResult:

        query_embedding = self.embedding_model.embed_query(
            question,
        )

        metadata = self.metadata_extractor.extract(
    question,
)
        print("=" * 80)
        print("METADATA", metadata)
        print("=" * 80)

        where = MetadataFilter.to_chroma_where(
            metadata,
)
        print("=" * 80)
        print("WHERE", where)
        print("=" * 80)
        

        candidate_count = max(
            top_k * 4,
            20,
        )
#         candidate_count = max(
#     top_k * 10,
#     50,
# )

        search_result = self.retriever.retrieve(
            query_embedding=query_embedding,
            question=question,
            where=where,  
            top_k=candidate_count,
        )

        children = []

        for idx, child_id in enumerate(search_result.ids):

            child_chunk = ingestion.child_lookup[child_id]

            child = RetrievedChild(
                id=child_chunk.id,
                parent_id=child_chunk.parent_id,
                content=child_chunk.content,
                metadata=child_chunk.metadata,
                score=search_result.scores[idx],
            )

            children.append(child)

        if self.reranker is not None:

            children = self.reranker.rerank(
                question=question,
                children=children,
                top_k=top_k,
            )

        else:

            children = children[:top_k]

        parents = {}

        for child in children:

            parent = ingestion.parent_lookup[
                child.parent_id
            ]

            parents[parent.id] = parent

        return RetrievalResult(
            children=children,
            parents=list(parents.values()),
        )