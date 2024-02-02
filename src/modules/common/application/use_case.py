from abc import ABC, abstractmethod
from typing import Any


__all__ = [
    "UseCase",
]

class UseCase(ABC):
    @abstractmethod 
    def __init__(self) -> None:
        ...

    @abstractmethod
    async def execute(self) -> Any:
        ...
