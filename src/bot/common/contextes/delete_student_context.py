from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

__all__ = [
    "DeleteStudentContext",
]


class DeleteStudentContext:
    """Just adapter to FSMContext."""

    _context: FSMContext

    def __init__(self, context: FSMContext) -> None:
        self._context = context

    @property
    async def telegram_id(self) -> int:
        telegram_id = (await self._context.get_data())["telegram_id"]
        assert telegram_id is not None, "You must have set telegram before."
        return telegram_id

    async def set_telegram_id(self, telegram_id: int) -> None:
        await self._context.update_data(telegram_id=telegram_id)

    @property
    async def last_name(self) -> str:
        last_name = (await self._context.get_data())["last_name"]
        assert last_name is not None, "You must have set last_name before."
        return last_name

    async def set_last_name(self, last_name: str) -> None:
        await self._context.update_data(last_name=last_name)

    @property
    async def first_name(self) -> str:
        first_name = (await self._context.get_data())["first_name"]
        assert first_name is not None, "You must have set first_name before."
        return first_name

    async def set_first_name(self, first_name: str) -> None:
        await self._context.update_data(first_name=first_name)

    @property
    async def group_name(self) -> str:
        group_name = (await self._context.get_data())["group_name"]
        assert group_name is not None, "You must have set group_name before."
        return group_name

    async def set_group_name(self, group_name: str) -> None:
        await self._context.update_data(group_name=group_name)

    async def set_state(self, state: StateType = None) -> None:
        await self._context.set_state(state)

    async def clear(self) -> None:
        await self._context.set_state(state=None)
        await self._context.set_data({})
