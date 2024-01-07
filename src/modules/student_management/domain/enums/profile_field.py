from enum import UNIQUE, StrEnum, verify

__all__ = [
    "ProfileField",
]


@verify(UNIQUE)
class ProfileField(StrEnum):
    SURNAME = "surname"
    NAME = "name"
