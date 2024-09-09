from typing import Self
from enum import StrEnum, verify, UNIQUE

__all__ = [
    "NSTULessonType",
]


@verify(UNIQUE)
class NSTULessonType(StrEnum):
    LECTION = "ЛК"
    PRACTISE = "ПР"
    LABORATORY = "ЛБ"
    NOTHING = ""

    @classmethod
    def from_name(cls, name: str) -> Self:
        match name.strip():
            case "Лекция":
                return cls.LECTION
            case "Практика":
                return cls.PRACTISE
            case "Лабораторная":
                return cls.LABORATORY
            case _:
                return cls.NOTHING

    @property
    def formatted(self) -> str:
        if self.value:
            return self.value + "\t"
        return ""
