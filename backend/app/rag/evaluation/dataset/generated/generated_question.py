from dataclasses import dataclass


@dataclass
class GeneratedQuestion:

    question: str

    expected_answer: str

    expected_sources: list[str]