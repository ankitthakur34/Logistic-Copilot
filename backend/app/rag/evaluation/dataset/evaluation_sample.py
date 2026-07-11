from dataclasses import dataclass


@dataclass
class EvaluationSample:

    question: str

    expected_answer: str

    expected_sources: list[str]