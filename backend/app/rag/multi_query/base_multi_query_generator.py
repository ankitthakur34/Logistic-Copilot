from abc import ABC, abstractmethod


class BaseMultiQueryGenerator(ABC):

    @abstractmethod
    def generate(
        self,
        question: str,
    ) -> list[str]:
        pass