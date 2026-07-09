from app.rag.metadata.metadata_filter import MetadataFilter
from app.rag.metadata.regex_metadata_extractor import (
    RegexMetadataExtractor,
)

from app.rag.schema.retrieval_result import (
    RetrievalResult,
    RetrievedChild,
)

from app.rag.metadata.metadata_extraction_pipeline import MetadataExtractionPipeline
from app.rag.metadata.llm_metadata_extractor import LLMMetadataExtractor
from app.rag.llm.groq_llm import GroqLLM


class RetrievalPipeline:

    def __init__(
        self,
        retriever,
        reranker=None,
        metadata_pipeline=None,
    ):

        self.retriever = retriever

        self.reranker = reranker

        self.metadata_pipeline = (
            metadata_pipeline
            or MetadataExtractionPipeline(
                regex_extractor=RegexMetadataExtractor(),
                llm_extractor=LLMMetadataExtractor(
                    llm=GroqLLM(),
                )
            )
        )

    def run(
        self,
        question: str,
        ingestion,
        top_k: int = 5,
    ) -> RetrievalResult:

        metadata = self.metadata_pipeline.extract(
    question,
    ingestion,
)

        where = MetadataFilter.to_chroma_where(
            metadata,
        )

        candidate_count = max(
            top_k * 4,
            20,
        )

        search_result = self.retriever.retrieve(
            question=question,
            where=where,
            top_k=candidate_count,
        )

        children = []

        for idx, child_id in enumerate(search_result.ids):

            child_chunk = ingestion.child_lookup[child_id]

            children.append(

                RetrievedChild(

                    id=child_chunk.id,

                    parent_id=child_chunk.parent_id,

                    content=child_chunk.content,
                    child_index=child_chunk.child_index,

                    metadata=child_chunk.metadata,

                    

                    score=search_result.scores[idx],
                    

                )

            )

        if self.reranker:

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