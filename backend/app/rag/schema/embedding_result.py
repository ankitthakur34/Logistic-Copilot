from dataclasses import dataclass, field

from app.rag.schema.ingestion_result import IngestionResult


@dataclass
class EmbeddedChunk:

    id: str

    content: str

    metadata: dict

    parent_id: str

    embedding: list[float]


@dataclass
class EmbeddingResult:

    ingestion: IngestionResult

    embedded_chunks: list[EmbeddedChunk]

    embedding_lookup: dict[str, EmbeddedChunk] = field(
        default_factory=dict
    )