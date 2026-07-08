from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Document:

    content: str

    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ParentChunk:
    id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChildChunk:
    id: str
    parent_id: str
    content: str
    child_index: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    
