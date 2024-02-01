from abc import ABC, abstractmethod

from injector import inject

__all__ = [
    "UseCase",
]

class UseCase(ABC):
    @inject
    @abstractmethod 
    def __init__(self) -> None:
        ...


    @abstractmethod
    async def execute(self) -> None:
        ...
