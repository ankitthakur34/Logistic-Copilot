from app.rag.schema.embedding_result import EmbeddingResult
from app.rag.schema.index_result import IndexResult
from app.rag.vector_store.base_vector_store import BaseVectorStore


class IndexPipeline:

    def __init__(
        self,
        vector_store: BaseVectorStore,
    ):

        self.vector_store = vector_store

    def run(
        self,
        embedding_result: EmbeddingResult,
    ) -> IndexResult:

        self.vector_store.index(
            embedding_result
        )

        return IndexResult(

            embedding_result=embedding_result,

            collection_name=self.vector_store.collection_name,

            total_vectors=len(
                embedding_result.embedded_chunks
            ),
        )