from app.rag.embeddings.base_embedding import BaseEmbedding
from app.rag.cache.base_cache import BaseCache
from app.rag.schema.embedding_result import (
    EmbeddedChunk,
    EmbeddingResult,
)
from app.rag.schema.ingestion_result import IngestionResult
from app.rag.constants import EMBEDDING_CACHE_KEY,DOCUMENT_CACHE_KEY, CHUNK_CACHE_KEY


class EmbeddingPipeline:

    def __init__(
        self,
        embedding_model: BaseEmbedding,
        cache: BaseCache | None = None,
    ):

        self.embedding_model = embedding_model
        self.cache = cache

    def get_or_compute(
        self,
        key,
        compute_fn,
    ):

        if self.cache is None:
            return compute_fn()

        if self.cache.exists(key):
            print(f"[CACHE] Loading '{key}'")

            return self.cache.load(key)

        print(f"[CACHE] Computing '{key}'")

        result = compute_fn()

        self.cache.save(
            key,
            result,
        )

        return result

    def run(
        self,
        ingestion: IngestionResult,
    ) -> EmbeddingResult:

        embedded_chunks = self.get_or_compute(
            EMBEDDING_CACHE_KEY,
            lambda: self._embed_chunks(
                ingestion
            ),
        )

        lookup = {

    embedded.id: embedded

    for embedded in embedded_chunks

}

        return EmbeddingResult(
            ingestion=ingestion,
            embedded_chunks=embedded_chunks,
            embedding_lookup=lookup,
        )

    
    def _embed_chunks(
    self,
    ingestion: IngestionResult,
):

        texts = [

        chunk.content

        for chunk in ingestion.child_chunks

    ]

        vectors = self.embedding_model.embed_documents(
        texts
    )

        embedded_chunks = []

        for chunk, vector in zip(

        ingestion.child_chunks,

        vectors,

    ):

            embedded_chunks.append(

            EmbeddedChunk(

                id=chunk.id,

                content=chunk.content,

                metadata=chunk.metadata,

                parent_id=chunk.parent_id,

                embedding=vector,

            )

        )

        return embedded_chunks