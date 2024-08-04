from datetime import date
from typing import TypedDict

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType

from src.modules.common.domain.university_alias import UniversityAlias
from src.modules.student_management.domain import Role

__all__ = [
    "RegistrationContext",
]


class RegistrationData(TypedDict, total=False):
    telegram_id: int
    role: Role
    group_name: str
    first_name: str
    last_name: str
    university_alias: UniversityAlias
    birthdate: date | None


class RegistrationContext:
    """Just adapter to FSMContext."""

    _context: FSMContext

    def __init__(self, context: FSMContext) -> None:
        self._context = context

    @property
    async def telegram_id(self) -> int:
        telegram_id = (await self.get_data()).get("telegram_id", None)
        assert telegram_id is not None, "You must have set telegram_id before."
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
    async def group_name(self) -> str:
        group_name = (await self.get_data()).get("group_name", None)
        assert group_name is not None, "You must have set group_name before."
        return group_name

    async def set_group_name(self, group_name: str) -> None:
        await self._context.update_data(group_name=group_name)

    @property
    async def last_name(self) -> str:
        last_name = (await self.get_data()).get("last_name", None)
        assert last_name is not None, "You must have set last_name before."
        return last_name

    async def set_last_name(self, last_name: str) -> None:
        await self._context.update_data(last_name=last_name)

    @property
    async def first_name(self) -> str:
        first_name = (await self.get_data()).get("first_name", None)
        assert first_name is not None, "You must have set first_name before."
        return first_name

    async def set_first_name(self, first_name: str) -> None:
        await self._context.update_data(first_name=first_name)

    @property
    async def university_alias(self) -> UniversityAlias:
        university_alias = (await self.get_data()).get("university_alias", None)
        assert university_alias is not None, "You must have set university_alias before."
        return university_alias

    async def set_university_alias(self, university_alias: UniversityAlias) -> None:
        await self._context.update_data(university_alias=university_alias)

    @property
    async def birthdate(self) -> date | None:
        return (await self.get_data()).get("birthdate", None)

    async def set_birthday(self, birthdate: date | None) -> None:
        await self._context.update_data(birthdate=birthdate)

    async def set_state(self, state: StateType = None) -> None:
        await self._context.set_state(state)

    async def clear(self) -> None:
        await self._context.set_state(state=None)
        await self._context.set_data({})

    async def get_data(self) -> RegistrationData:
<<<<<<< HEAD
        return await self._context.get_data()  # pyright: ignore[reportGeneralTypeIssues]
=======
        res = await self._context.get_data()

        if res.get("role", None) is not None:
            res["role"] = Role(res["role"])

        if res.get("university_alias", None) is not None:
            res["university_alias"] = UniversityAlias(res["university_alias"])

        return res  # pyright: ignore[reportReturnType]
>>>>>>> create_connection_abstraction
