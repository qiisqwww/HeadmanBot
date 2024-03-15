from datetime import date
from typing import TypedDict

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

__all__ = [
    "ProfileUpdateContext",
]


class NewProfileData(TypedDict, total=False):
    new_first_name: str
    new_last_name: str
    new_birthdate: date | None


class ProfileUpdateContext:
    """Just adapter to FSMContext."""

    _context: FSMContext

    def __init__(self, context: FSMContext) -> None:
        self._context = context

    @property
    async def new_first_name(self) -> str:
        new_first_name = (await self.get_data()).get("new_first_name", None)
        assert new_first_name is not None, "You must have settled new_first_name before."
        return new_first_name

    async def set_new_first_name(self, new_first_name: str) -> None:
        await self._context.update_data(new_first_name=new_first_name)

    @property
    async def new_last_name(self) -> str:
        new_last_name = (await self.get_data()).get("new_last_name", None)
        assert new_last_name is not None, "You must have settled new_last_name before."
        return new_last_name

    async def set_new_last_name(self, new_last_name: str) -> None:
        await self._context.update_data(new_last_name=new_last_name)

    @property
    async def new_birthdate(self) -> date | None:
        return (await self.get_data()).get("new_birthdate", None)

    async def set_new_birthdate(self, new_birthdate: date | None) -> None:
        await self._context.update_data(new_birthdate=new_birthdate)

    async def set_state(self, state: StateType = None) -> None:
        await self._context.set_state(state)

    async def get_data(self) -> NewProfileData:
        return await self._context.get_data()  # pyright: ignore[reportGeneralTypeIssues]

    async def clear(self) -> None:
        await self._context.set_state(state=None)
        await self._context.set_data({})
