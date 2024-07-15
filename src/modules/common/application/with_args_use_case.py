from abc import abstractmethod
from typing import Any

from .use_case import UseCase

__all__ = [
    "WithArgsUseCase",
]


class WithArgsUseCase(UseCase):
    @abstractmethod
    def execute(self, *args: object) -> Any:  # noqa: ANN401
        ...
