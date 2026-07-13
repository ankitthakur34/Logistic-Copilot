from app.rag.metadata.metadata_filter import (
    MetadataFilter,
)

from app.rag.metadata.regex_metadata_extractor import (
    RegexMetadataExtractor,
)

from app.rag.schema.retrieval_result import (
    RetrievalResult,
    RetrievedChild,
)

from app.rag.metadata.metadata_extraction_pipeline import (
    MetadataExtractionPipeline,
)

from app.rag.metadata.llm_metadata_extractor import (
    LLMMetadataExtractor,
)

from app.rag.llm.groq_llm import (
    GroqLLM,
)

# from app.rag.metadata.dictionary_metadata_extractor import (
#     DictionaryMetadataExtractor,
# )


class RetrievalPipeline:

    def __init__(

        self,

        retriever,

        reranker=None,

        metadata_pipeline=None,

        decomposition_pipeline=None,

    ):

        self.retriever = retriever

        self.reranker = reranker

        self.decomposition_pipeline = (
            decomposition_pipeline
        )

        self.metadata_pipeline = (

            metadata_pipeline

            or MetadataExtractionPipeline(

                regex_extractor=RegexMetadataExtractor(),

                # dictionary_extractor=DictionaryMetadataExtractor(),

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

        #
        # Query decomposition
        #

        questions = [
            question,
        ]

        if self.decomposition_pipeline:

            questions = (

                self.decomposition_pipeline.run(
                    question
                )

            )

        print()
        print("=" * 80)
        print("DECOMPOSED QUESTIONS")
        print("=" * 80)

        for q in questions:

            print(q)

        print()

        #
        # Retrieve for every sub-question
        #

        all_ids = []

        all_scores = []

        for sub_question in questions:

            metadata = (

                self.metadata_pipeline.extract(

                    sub_question,

                    ingestion,

                )

            )

            where = (

                MetadataFilter.to_chroma_where(
                    metadata,
                )

            )

            print()
            print("=" * 80)
            print("SUB QUESTION")
            print("=" * 80)

            print(sub_question)

            print()

            print("WHERE FILTER")

            print(where)

            print()

            candidate_count = max(

                top_k * 4,

                20,

            )

            result = self.retriever.retrieve(

                question=sub_question,

                where=where,

                top_k=candidate_count,

            )

            all_ids.extend(
                result.ids
            )

            all_scores.extend(
                result.scores
            )

        #
        # Merge duplicate children
        #

        merged = {}

        for idx, child_id in enumerate(
            all_ids
        ):

            score = all_scores[idx]

            if child_id not in merged:

                merged[
                    child_id
                ] = score

            else:

                merged[
                    child_id
                ] = max(

                    merged[
                        child_id
                    ],

                    score,

                )

        merged = sorted(

            merged.items(),

            key=lambda x: x[1],

            reverse=True,

        )

        print()
        print("=" * 80)
        print("MERGED CHILDREN")
        print("=" * 80)

        for child_id, score in merged:

            print(
                child_id,
                score,
            )

        #
        # Build children
        #

        children = []

        for child_id, score in merged:

            child_chunk = (

                ingestion.child_lookup[
                    child_id
                ]

            )

            children.append(

                RetrievedChild(

                    id=child_chunk.id,

                    parent_id=child_chunk.parent_id,

                    content=child_chunk.content,

                    child_index=child_chunk.child_index,

                    metadata=child_chunk.metadata,

                    score=score,

                )

            )

        #
        # Rerank
        #

        if self.reranker:

            children = (

                self.reranker.rerank(

                    question=question,

                    children=children,

                    top_k=top_k,

                )

            )

        else:

            children = children[:top_k]

        #
        # Parent aggregation
        #

        parents = {}

        for child in children:

            parent = (

                ingestion.parent_lookup[
                    child.parent_id
                ]

            )

            parents[
                parent.id
            ] = parent

        return RetrievalResult(

            children=children,

            parents=list(
                parents.values()
            ),

        )