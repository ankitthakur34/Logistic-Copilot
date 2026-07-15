from dataclasses import dataclass
from typing import Any


@dataclass
class SQLResult:

    question: str

    sql: str

    rows: list[dict[str, Any]]