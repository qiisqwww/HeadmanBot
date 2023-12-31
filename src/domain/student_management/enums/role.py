from enum import UNIQUE, EnumMeta, StrEnum, verify
from typing import Self

__all__ = [
    "Role",
]


class EnumContainsMeta(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)

        except ValueError:
            return False

        return True


@verify(UNIQUE)
class Role(StrEnum, metaclass=EnumContainsMeta):
    ADMIN = "admin"
    HEADMAN = "headman"
    VICE_HEADMAN = "vice headman"
    STUDENT = "student"

    @property
    def translation(self) -> str:
        translations = {
            Role.ADMIN: "Админ",
            Role.HEADMAN: "Староста",
            Role.VICE_HEADMAN: "Заместитель старосты",
            Role.STUDENT: "Студент",
        }

        return translations[self]

    @property
    def _weight(self) -> int:
        roles_weight = {
            "ADMIN": 4,
            "HEADMAN": 3,
            "VICE_HEADMAN": 2,
            "STUDENT": 1,
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
