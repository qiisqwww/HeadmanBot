from typing import Self
from enum import StrEnum, verify, UNIQUE

from loguru import logger

__all__ = [
    "LessonType",
]


@verify(UNIQUE)
class LessonType(StrEnum):
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
