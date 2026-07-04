from abc import ABC, abstractmethod


class BaseCache(ABC):

    @abstractmethod
    def save(
        self,
        key: str,
        data,
    ) -> None:
        pass

    @abstractmethod
    def load(
        self,
        key: str,
    ):
        pass

    @abstractmethod
    def exists(
        self,
        key: str,
    ) -> bool:
        pass

    @abstractmethod
    def delete(
        self,
        key: str,
    ) -> None:
        pass