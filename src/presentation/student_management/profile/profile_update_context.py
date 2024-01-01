from abc import ABC, abstractmethod
from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

__all__ = [
    "ProfileUpdateContext",
]


class ProfileUpdateContext(ABC):
    """Just adapter to FSMContext."""

    @abstractmethod
    def __init__(self, context: FSMContext) -> None:
        ...

    @property
    @abstractmethod
    async def telegram_id(self) -> int:
        ...

    @abstractmethod
    async def set_telegram_id(self, telegram_id: int) -> None:
        ...

    @property
    @abstractmethod
    async def surname(self) -> str:
        ...

    @abstractmethod
    async def set_surname(self, surname: str) -> None:
        ...

    @property
    @abstractmethod
    async def name(self) -> str:
        ...

    @abstractmethod
    async def set_name(self, name: str) -> None:
        ...

    @abstractmethod
    async def set_state(self, state: StateType = None) -> None:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...

    @abstractmethod
    async def get_data(self) -> dict[str, Any]:
        ...
