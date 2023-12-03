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
    ADMIN = "Админ"
    HEADMAN = "Староста"
    VICE_HEADMAN = "Заместитель cтаросты"
    STUDENT = "Студент"

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

        return self._weight() > other._weight()

    def __ge__(self, other: Self) -> bool:  # type: ignore
        if not isinstance(other, Role):
            raise NotImplementedError

        return self._weight() >= other._weight()

    def __lt__(self, other: Self) -> bool:  # type: ignore
        if not isinstance(other, Role):
            raise NotImplementedError

        return self._weight() < other._weight()

    def __le__(self, other: Self) -> bool:  # type: ignore
        if not isinstance(other, Role):
            raise NotImplementedError

        return self._weight() <= other._weight()
