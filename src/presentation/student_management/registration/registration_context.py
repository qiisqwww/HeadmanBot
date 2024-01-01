from abc import ABC, abstractmethod
from datetime import date
from typing import Any

from aiogram.fsm.storage.base import StateType

from src.domain.edu_info import UniversityAlias
from src.domain.student_management import Role

__all__ = [
    "RegistrationContext",
]


class RegistrationContext(ABC):
    """Just adapter to FSMContext."""

    @property
    @abstractmethod
    async def telegram_id(self) -> int:
        ...

    @abstractmethod
    async def set_telegram_id(self, telegram_id: int) -> None:
        ...

    @property
    @abstractmethod
    async def role(self) -> Role:
        ...

    @abstractmethod
    async def set_role(self, role: Role) -> None:
        ...

    @property
    @abstractmethod
    async def group_name(self) -> str:
        ...

    @abstractmethod
    async def set_group_name(self, group_name: str) -> None:
        ...

    @property
    @abstractmethod
    async def surname(self) -> str:
        ...

    @abstractmethod
    async def set_surname(self, surname: str) -> None:
        ...

    @property
    @abstractmethod
    async def name(self) -> str:
        ...

    @abstractmethod
    async def set_name(self, name: str) -> None:
        ...

    @property
    @abstractmethod
    async def university_alias(self) -> UniversityAlias:
        ...

    @abstractmethod
    async def set_university_alias(self, university_alias: UniversityAlias) -> None:
        ...

    @property
    @abstractmethod
    async def birthdate(self) -> date | None:
        ...

    @abstractmethod
    async def set_birthday(self, birthdate: date | None) -> None:
        ...

    @abstractmethod
    async def set_state(self, state: StateType = None) -> None:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...

    @abstractmethod
    async def get_data(self) -> dict[str, Any]:
        ...
