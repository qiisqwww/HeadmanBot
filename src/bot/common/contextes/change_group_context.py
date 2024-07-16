from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType


__all__ = [
    "ChangeGroupContext",
]


class ChangeGroupContext:
    """Just adapter to FSMContext."""

    _context: FSMContext

    def __init__(self, context: FSMContext) -> None:
        self._context = context

    async def set_state(self, state: StateType = None) -> None:
        await self._context.set_state(state)

    async def clear(self) -> None:
        await self._context.set_state(state=None)
        await self._context.set_data({})
