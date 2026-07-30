from dataclasses import dataclass
from typing import Any


@dataclass
class SQLAnswerResult:

    question: str

    sql: str
    normalized_sql:str

    answer: str

    rows: list[dict[str, Any]]