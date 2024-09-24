from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

from src.modules.common.domain.university_alias import UniversityAlias

__all__ = [
    "ChangeGroupAdminContext",
]


class ChangeGroupAdminContext:
    """Just adapter to FSMContext."""

    _context: FSMContext

    def __init__(self, context: FSMContext) -> None:
        self._context = context

    async def set_state(self, state: StateType = None) -> None:
        await self._context.set_state(state)

    @property
    async def university_id(self) -> int:
        university_id = (await self._context.get_data()).get("university_id", None)
        assert university_id is not None, "You must have set university_id before."
        return UniversityAlias(university_id)

    async def set_university_id(self, university_id: int) -> None:
        await self._context.update_data(university_id=university_id)

    async def clear(self) -> None:
        await self._context.set_state(state=None)
        await self._context.set_data({})
