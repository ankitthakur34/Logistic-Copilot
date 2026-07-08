from app.rag.generation.answer_generator import AnswerGenerator


class AnswerPipeline:

    def __init__(

        self,

        retrieval_pipeline,

        answer_generator: AnswerGenerator,

    ):

        self.retrieval_pipeline = retrieval_pipeline

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

        return self.answer_generator.generate(

            question=question,

            retrieval=retrieval,

        )