from abc import ABC, abstractmethod


class BaseQueryDecomposer(ABC):

    @abstractmethod
    def decompose(
        self,
        question: str,
    ) -> list[str]:
        pass