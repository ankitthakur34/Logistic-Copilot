from app.rag.generation.answer_generator import AnswerGenerator
from app.rag.context_compression.context_compression_pipeline import (
    ContextCompressionPipeline,
)


class AnswerPipeline:

    def __init__(

        self,

        retrieval_pipeline,
        context_compression_pipeline: ContextCompressionPipeline,

        answer_generator: AnswerGenerator,

    ):

        self.retrieval_pipeline = retrieval_pipeline
        # compression pipeline to compress the retrieval results before generating the answer
        self.context_compression_pipeline = context_compression_pipeline

        self.answer_generator = answer_generator

    def run(

        self,

        question: str,

        ingestion,

        top_k: int = 5,

    ):

        retrieval = self.retrieval_pipeline.run(

            question=question,

            ingestion=ingestion,

            top_k=top_k,

        )

        print("=" * 80)
        print("PARENTS RECEIVED FROM RETRIEVAL PIPELINE BEFORE COMPRESSION")
        print("=" * 80)

        for parent in retrieval.parents:
            print(parent.id)
            print(parent.content)
            print()
        # compress the retrieval results before generating the answer
        retrieval = self.context_compression_pipeline.run(

            retrieval,

        )

        print("=" * 80)
        print("PARENTS SENT TO LLM")
        print("=" * 80)

        for parent in retrieval.parents:
            print(parent.id)
            print(parent.content)
            print()

        return self.answer_generator.generate(

            question=question,

            retrieval=retrieval,

        )