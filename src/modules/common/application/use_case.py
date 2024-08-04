from abc import ABC, abstractmethod
from typing import Any

__all__ = [
    "UseCase",
    "NoArgsUseCase",
    "WithArgsUseCase",
]


class UseCase(ABC):  # noqa: B024
    ...


class NoArgsUseCase(UseCase):
    @abstractmethod
    def execute(self) -> Any:  # noqa: ANN401
        ...

class WithArgsUseCase(UseCase):
    @abstractmethod
    def execute(self, *args: object) -> Any:  # noqa: ANN401
        ...
