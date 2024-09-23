from typing import Self
from enum import StrEnum, verify, UNIQUE

__all__ = [
    "STULessonType",
]


@verify(UNIQUE)
class STULessonType(StrEnum):
    LECTION = "ЛК"
    PRACTISE = "ПР"
    LABORATORY = "ЛБ"
    NOTHING = ""

    @classmethod
    def from_name(cls, name: str) -> Self:
        match name.strip():
            case "Л":
                return cls.LECTION
            case "ПЗ":
                return cls.PRACTISE
            case "ЛР":
                return cls.LABORATORY
            case _:
                return cls.NOTHING

    @property
    def formatted(self) -> str:
        if self.value:
            return self.value + "\t"
        return ""
