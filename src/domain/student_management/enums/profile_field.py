from enum import UNIQUE, StrEnum, verify

__all__ = [
    "ProfileField",
]


@verify(UNIQUE)
class ProfileField(StrEnum):
    surname = "surname"
    name = "name"
