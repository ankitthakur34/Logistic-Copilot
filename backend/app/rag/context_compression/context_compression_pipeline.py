from app.rag.schema.retrieval_result import RetrievalResult

from app.rag.context_compression.base_context_compressor import (
    BaseContextCompressor,
)


class ContextCompressionPipeline:

    def __init__(
        self,
        compressor: BaseContextCompressor,
    ):
        self.compressor = compressor

    def run(
        self,
        retrieval: RetrievalResult,
    ) -> RetrievalResult:

        return self.compressor.compress(
            retrieval,
        )