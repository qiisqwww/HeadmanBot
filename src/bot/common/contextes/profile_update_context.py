from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

__all__ = [
    "ProfileUpdateContext",
]


class ProfileUpdateContext:
    """Just adapter to FSMContext."""

    _context: FSMContext

    def __init__(self, context: FSMContext) -> None:
        self._context = context

    @property
    async def telegram_id(self) -> int:
        telegram_id: int = (await self._context.get_data())["telegram_id"]
        return telegram_id

    async def set_telegram_id(self, telegram_id: int) -> None:
        await self._context.update_data(telegram_id=telegram_id)

    @property
    async def new_data(self) -> str:
        new_data: str = (await self._context.get_data())["surname"]
        return new_data

    async def set_new_data(self, surname: str) -> None:
        await self._context.update_data(surname=surname)

    async def set_state(self, state: StateType = None) -> None:
        await self._context.set_state(state)

    async def clear(self) -> None:
        await self._context.set_state(state=None)
        await self._context.set_data({})

    async def get_data(self) -> dict[str, Any]:
        data: dict[str, Any] =  await self._context.get_data()
        return data
