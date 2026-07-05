from dataclasses import dataclass

from app.rag.context.context_result import ContextResult


@dataclass
class RAGResponse:

    answer: str

    context: ContextResult

    prompt: str

    model: str

    usage: dict | None = None