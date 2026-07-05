from app.rag.ingestion.ingest_pipeline import (
    IngestionPipeline,
)

from app.rag.retrieval.retrieval_pipeline import (
    RetrievalPipeline,
)

from app.rag.context.base_context_builder import (
    BaseContextBuilder,
)

from app.rag.prompts.base_prompt_builder import (
    BasePromptBuilder,
)

from app.rag.llm.base_llm import (
    BaseLLM,
)

from app.rag.service.rag_response import (
    RAGResponse)


class RAGService:

    def __init__(

        self,

        ingestion_pipeline: IngestionPipeline,

        retrieval_pipeline: RetrievalPipeline,

        context_builder: BaseContextBuilder,

        prompt_builder: BasePromptBuilder,

        llm: BaseLLM,

    ):

        self.ingestion_pipeline = ingestion_pipeline

        self.retrieval_pipeline = retrieval_pipeline

        self.context_builder = context_builder

        self.prompt_builder = prompt_builder

        self.llm = llm

        self.ingestion = None

    def initialize(self):

        """
        Load documents only once.
        """

        if self.ingestion is None:

            self.ingestion = self.ingestion_pipeline.run()

    def ask(

        self,

        question: str,

    ) -> RAGResponse:

        self.initialize()

        retrieval = self.retrieval_pipeline.run(

            question=question,

            ingestion=self.ingestion,

        )

        context = self.context_builder.build(

            retrieval,

        )

        prompt = self.prompt_builder.build(

            question=question,

            context=context,

        )

        llm_result = self.llm.generate(

            prompt,

        )

        return RAGResponse(

            answer=llm_result.answer,

            context=context,

            prompt=prompt,

            model=llm_result.model,

            usage=llm_result.usage,

        )