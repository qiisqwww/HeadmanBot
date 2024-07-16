from typing import TypedDict

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

from src.modules.student_management.domain import Role
from src.modules.common.domain.university_alias import UniversityAlias


__all__ = [
    "ChangeGroupContext",
]


class ChangeGroupData(TypedDict, total=False):
    telegram_id: int
    new_role: Role
    university_alias: UniversityAlias
    new_group_name: str
    first_name: str
    last_name: str


class ChangeGroupContext:
    """Just adapter to FSMContext."""

    _context: FSMContext

    def __init__(self, context: FSMContext) -> None:
        self._context = context

    @property
    async def new_role(self) -> Role:
        new_role = (await self.get_data()).get("new_role", None)
        assert new_role is not None, "You must have set new role before."
        return new_role

    async def set_new_role(self, new_role: Role) -> None:
        await self._context.update_data(new_role=new_role)

    @property
    async def new_group_name(self) -> str | None:
        new_group_name = (await self.get_data()).get("new_group_name", None)
        return new_group_name

    async def set_new_group_name(self, new_group_name: str) -> None:
        await self._context.update_data(new_group_name=new_group_name)

    @property
    async def university_alias(self) -> UniversityAlias:
        university_alias = (await self.get_data()).get("university_alias", None)
        assert university_alias is not None, "You must have set university_alias before."
        return university_alias

    async def set_university_alias(self, university_alias: UniversityAlias) -> None:
        await self._context.update_data(university_alias=university_alias)

    async def get_data(self) -> ChangeGroupData:
        return await self._context.get_data()  # pyright: ignore[reportGeneralTypeIssues]

    async def set_state(self, state: StateType = None) -> None:
        await self._context.set_state(state)

    async def clear(self) -> None:
        await self._context.set_state(state=None)
        await self._context.set_data({})
