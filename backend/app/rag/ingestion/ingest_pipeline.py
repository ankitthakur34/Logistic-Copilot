from typing import Callable, Any

from app.rag.loader.base_loader import BaseLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.schema.ingestion_result import IngestionResult


class IngestionPipeline:

    def __init__(
        self,
        loader: BaseLoader,
        chunker: ParentChildChunker,
      
    ):

        self.loader = loader
        self.chunker = chunker
       

    

    def run(self) -> IngestionResult:

        # -----------------------------
        # Load Documents
        # -----------------------------
        documents = self.loader.load()


        # -----------------------------
        # Chunk Documents
        # -----------------------------
        parent_chunks, child_chunks = (
    self.chunker.chunk_documents(
        documents
    )
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