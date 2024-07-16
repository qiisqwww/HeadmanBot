from enum import UNIQUE, StrEnum, verify
from typing import Self

__all__ = [
    "Role",
]


@verify(UNIQUE)
class Role(StrEnum):
    ADMIN = "ADMIN"
    HEADMAN = "HEADMAN"
    VICE_HEADMAN = "VICE HEADMAN"
    STUDENT = "STUDENT"
    IS_REGISTERED = "IS REGISTERED"

    @property
    def translation(self) -> str:
        translations = {
            Role.ADMIN: "Админ",
            Role.HEADMAN: "Староста",
            Role.VICE_HEADMAN: "Заместитель старосты",
            Role.STUDENT: "Студент",
            Role.IS_REGISTERED: "Зарегестрирован"
        }

        return translations[self]

    @property
    def _weight(self) -> int:
        roles_weight = {
            "ADMIN": 4,
            "HEADMAN": 3,
            "VICE_HEADMAN": 2,
            "STUDENT": 1,
            "IS_REGISTERED": 0,
        }

        return roles_weight[self.name]

    def __gt__(self, other: Self) -> bool:  # type: ignore
        if not isinstance(other, Role):
            raise NotImplementedError

        return self._weight > other._weight

    def __ge__(self, other: Self) -> bool:  # type: ignore
        if not isinstance(other, Role):
            raise NotImplementedError

        return self._weight >= other._weight

    def __lt__(self, other: Self) -> bool:  # type: ignore
        if not isinstance(other, Role):
            raise NotImplementedError

        return self._weight < other._weight

    def __le__(self, other: Self) -> bool:  # type: ignore
        if not isinstance(other, Role):
            raise NotImplementedError

        return self._weight <= other._weight
