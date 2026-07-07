from abc import ABC, abstractmethod

from app.rag.metadata.metadata_result import MetadataResult


class BaseMetadataExtractor(ABC):

    @abstractmethod
    def extract(
        self,
        question: str,
    ) -> MetadataResult:
        pass