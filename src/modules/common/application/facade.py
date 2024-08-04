from abc import abstractmethod
from typing import Any

from .use_case import NoArgsUseCase, WithArgsUseCase

__all__ = [
    "Facade",
]

class Facade(NoArgsUseCase):
    @abstractmethod
    async def run_command_isolated(self, action_type: type[NoArgsUseCase | WithArgsUseCase], *args: Any) -> None:
        ...
