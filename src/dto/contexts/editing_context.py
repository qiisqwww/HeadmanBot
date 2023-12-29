from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

__all__ = [
    "EditingContext",
]


class EditingContext:
    """Just adapter to FSMContext."""

    _context: FSMContext

    def __init__(self, context: FSMContext) -> None:
        self._context = context

    @property
    async def telegram_id(self) -> int:
        return (await self._context.get_data())["telegram_id"]

    async def set_telegram_id(self, telegram_id: int) -> None:
        await self._context.update_data(telegram_id=telegram_id)

    @property
    async def surname(self) -> str:
        return (await self._context.get_data())["surname"]

    async def set_surname(self, surname: str) -> None:
        await self._context.update_data(surname=surname)

    @property
    async def name(self) -> str:
        return (await self._context.get_data())["name"]

    async def set_name(self, name: str) -> None:
        await self._context.update_data(name=name)

    async def set_state(self, state: StateType = None) -> None:
        await self._context.set_state(state)

    async def clear(self) -> None:
        await self._context.set_state(state=None)
        await self._context.set_data({})

    async def get_data(self) -> dict[str, Any]:
        return await self._context.get_data()
