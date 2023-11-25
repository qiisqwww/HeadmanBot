from enum import UNIQUE, StrEnum, verify

__all__ = [
    "UniversityAlias",
]


@verify(UNIQUE)
class UniversityAlias(StrEnum):
    MIREA = "MIREA"
    BMSTU = "BMSTU"
