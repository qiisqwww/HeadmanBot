from abc import abstractmethod
from typing import Any

from .use_case import UseCase

__all__ = [
    "NoArgsUseCase",
]


class NoArgsUseCase(UseCase):
    @abstractmethod
    def execute(self) -> Any:  # noqa: ANN401
        ...
