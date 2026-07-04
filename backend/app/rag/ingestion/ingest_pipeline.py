from typing import Callable, Any

from app.rag.loader.base_loader import BaseLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.cache.base_cache import BaseCache
from app.rag.schema.ingestion_result import IngestionResult


class IngestionPipeline:

    def __init__(
        self,
        loader: BaseLoader,
        chunker: ParentChildChunker,
        cache: BaseCache | None = None,
    ):

        self.loader = loader
        self.chunker = chunker
        self.cache = cache

    def get_or_compute(
        self,
        key: str,
        compute_fn: Callable[[], Any],
    ) -> Any:

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

    def run(self) -> IngestionResult:

        # -----------------------------
        # Load Documents
        # -----------------------------
        documents = self.get_or_compute(
            "documents",
            self.loader.load,
        )

        # -----------------------------
        # Chunk Documents
        # -----------------------------
        parent_chunks, child_chunks = self.get_or_compute(
            "chunks",
            lambda: self.chunker.chunk_documents(
                documents
            ),
        )

        # -----------------------------
        # Parent Lookup
        # -----------------------------
        parent_lookup = {
            parent.id: parent
            for parent in parent_chunks
        }

        # -----------------------------
        # Child Lookup
        # -----------------------------
        child_lookup = {
            child.id: child
            for child in child_chunks
        }

        # -----------------------------
        # Return Pipeline Result
        # -----------------------------
        return IngestionResult(
            documents=documents,
            parent_chunks=parent_chunks,
            child_chunks=child_chunks,
            parent_lookup=parent_lookup,
            child_lookup=child_lookup,
        )