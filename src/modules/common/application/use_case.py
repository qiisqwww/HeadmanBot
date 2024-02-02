from abc import ABC, abstractmethod


__all__ = [
    "UseCase",
]

class UseCase(ABC):
    @abstractmethod 
    def __init__(self) -> None:
        ...


    @abstractmethod
    async def execute(self) -> None:
        ...
