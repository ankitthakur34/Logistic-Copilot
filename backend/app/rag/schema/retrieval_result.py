from dataclasses import dataclass

from app.rag.schema.document import ParentChunk


@dataclass
class RetrievedChild:

    id: str

    parent_id: str

    content: str
    child_index: int

    metadata: dict

    

    score: float


@dataclass
class RetrievalResult:

    children: list[RetrievedChild]

    parents: list[ParentChunk]