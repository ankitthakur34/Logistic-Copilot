from dataclasses import dataclass


@dataclass
class ContextResult:

    context: str

    sources: list[str]

    document_count: int