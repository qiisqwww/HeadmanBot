from typing import TypedDict

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

from src.modules.student_management.domain import Role, Student
from src.modules.common.domain.university_alias import UniversityAlias


__all__ = [
    "EnterGroupContext",
]


class EnterGroupData(TypedDict, total=False):
    telegram_id: int
    role: Role
    group_name: str
    university_alias: UniversityAlias


class EnterGroupContext:
    """Just adapter to FSMContext."""

    _context: FSMContext

    def __init__(self, context: FSMContext) -> None:
        self._context = context

    @property
    async def telegram_id(self) -> int:
        telegram_id = (await self.get_data()).get("telegram_id", None)
        assert id is not None, "You must have set telegram id before."
        return telegram_id

    async def set_telegram_id(self, telegram_id: int) -> None:
        await self._context.update_data(telegram_id=telegram_id)

    @property
    async def role(self) -> Role:
        role = (await self.get_data()).get("role", None)
        assert role is not None, "You must have set role before."
        return role

    async def set_role(self, role: Role) -> None:
        await self._context.update_data(role=role)

    @property
    async def group_name(self) -> str | None:
        group_name = (await self.get_data()).get("group_name", None)
        return group_name

    async def set_group_name(self, group_name: str) -> None:
        await self._context.update_data(group_name=group_name)

    @property
    async def university_alias(self) -> UniversityAlias:
        university_alias = (await self.get_data()).get("university_alias", None)
        assert university_alias is not None, "You must have set university_alias before."
        return university_alias

    async def set_university_alias(self, university_alias: UniversityAlias) -> None:
        await self._context.update_data(university_alias=university_alias)

    async def get_data(self) -> EnterGroupData:
        return await self._context.get_data()  # pyright: ignore[reportGeneralTypeIssues]

    async def set_state(self, state: StateType = None) -> None:
        await self._context.set_state(state)

    async def clear(self) -> None:
        await self._context.set_state(state=None)
        await self._context.set_data({})
