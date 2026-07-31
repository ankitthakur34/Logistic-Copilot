from enum import Enum


class RouterDecision(str, Enum):

    SQL = "sql"

    RAG = "rag"

    UNKNOWN = "unknown"