from app.rag.schema.index_result import IndexResult


class IndexPipeline:

    def __init__(
        self,
        vector_store,
    ):
        self.vector_store = vector_store

    def run(
        self,
        child_chunks,
        embeddings,
    ):

        self.vector_store.index(
            child_chunks=child_chunks,
            embeddings=embeddings,
        )

        return IndexResult(
            total_vectors=len(child_chunks),
        )