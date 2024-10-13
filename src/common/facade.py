from abc import ABC, abstractmethod
from typing import Any

from src.common.database.db_context import DbContext
from .use_case import NoArgsUseCase, WithArgsUseCase

__all__ = [
    "Facade",
]


class Facade(ABC):
    def __init__(self, pool) -> None:
        self._pool = pool

    async def run_command_isolated(self, action_type: type[NoArgsUseCase | WithArgsUseCase], *args: Any) -> None:
        async with DbContext(pool=self._pool) as con:
            action = action_type(con=con)
            await action.execute(*args)

    @abstractmethod
    async def execute(self) -> None:
        ...
