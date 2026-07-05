from dataclasses import dataclass


@dataclass
class LLMResult:

    answer: str

    model: str

    usage: dict | None = None