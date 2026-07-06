from dataclasses import dataclass


@dataclass
class SearchResult:

    ids: list[str]

    # documents: list[str]

    # metadatas: list[dict]

    scores: list[float]