from abc import ABC, abstractmethod

from app.rag.schema.document import Document


class BaseLoader(ABC):

    @abstractmethod
    def load(self) -> list[Document]:
        """
        Load documents from any source.

        Returns:
            List[Document]
        """
        pass