from enum import UNIQUE, StrEnum, verify

from .enum_contains_meta import EnumContainsMeta

__all__ = [
    "Role",
]


@verify(UNIQUE)
class Role(StrEnum, metaclass=EnumContainsMeta):
    HEADMAN = "Староста"
    STUDENT = "Студент"
