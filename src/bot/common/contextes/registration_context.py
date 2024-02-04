from datetime import date
from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

from src.modules.common.domain.university_alias import UniversityAlias
from src.modules.student_management.domain import Role

__all__ = [
    "RegistrationContext",
]


class RegistrationContext:
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
    async def role(self) -> Role:
        return (await self._context.get_data())["role"]

    async def set_role(self, role: Role) -> None:
        await self._context.update_data(role=role)

    @property
    async def group_name(self) -> str:
        return (await self._context.get_data())["group_name"]

    async def set_group_name(self, group_name: str) -> None:
        await self._context.update_data(group_name=group_name)

    @property
    async def new_data(self) -> str:
        return (await self._context.get_data())["new_data"]

    async def set_data(self, new_data: str) -> None:
        await self._context.update_data(new_data=new_data)

    @property
    async def university_alias(self) -> UniversityAlias:
        return (await self._context.get_data())["university_alias"]

    async def set_university_alias(self, university_alias: UniversityAlias) -> None:
        await self._context.update_data(university_alias=university_alias)

    @property
    async def birthdate(self) -> date | None:
        return (await self._context.get_data())["birthdate"]

    async def set_birthday(self, birthdate: date | None) -> None:
        await self._context.update_data(birthdate=birthdate)

    async def set_state(self, state: StateType = None) -> None:
        await self._context.set_state(state)

    async def clear(self) -> None:
        await self._context.set_state(state=None)
        await self._context.set_data({})

    async def get_data(self) -> dict[str, Any]:
        return await self._context.get_data()
