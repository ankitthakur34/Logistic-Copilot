from dataclasses import dataclass
from typing import List


@dataclass
class GeneratedQuestion:

    question: str

    expected_answer: str

    expected_sources: List[str]