from dataclasses import dataclass, field

from app.rag.schema.document import (
    Document,
    ParentChunk,
    ChildChunk,
)


@dataclass
class IngestionResult:

    documents: list[Document]

    parent_chunks: list[ParentChunk]

    child_chunks: list[ChildChunk]

    parent_lookup: dict[str, ParentChunk] = field(
        default_factory=dict
    )

    child_lookup: dict[str, ChildChunk] = field(
        default_factory=dict
    )