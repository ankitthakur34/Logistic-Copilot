from dataclasses import dataclass

from app.rag.schema.embedding_result import EmbeddingResult


@dataclass
class IndexResult:

    embedding_result: EmbeddingResult

    collection_name: str

    total_vectors: int