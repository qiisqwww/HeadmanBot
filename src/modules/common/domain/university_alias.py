from enum import StrEnum, unique

__all__ = [
    "UniversityAlias",
]


@unique
class UniversityAlias(StrEnum):
    MIREA = "MIREA"
    BMSTU = "BMSTU"
    NSTU = "NSTU"
    STU = "STU"
    MIIGAIK = 'MIIGAIK'
