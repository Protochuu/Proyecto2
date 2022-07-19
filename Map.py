from abc import ABC, abstractmethod


class Map(ABC):
    @abstractmethod
    def insert(self, key: str, value: int):
        pass

    @abstractmethod
    def erase(self, key: str):
        pass

    @abstractmethod
    def at(self, key: str) -> int:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def empty(self) -> bool:
        pass
