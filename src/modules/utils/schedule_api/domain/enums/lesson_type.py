from typing import Self
from enum import StrEnum, verify, UNIQUE

__all__ = [
    "LessonType",
]




@verify(UNIQUE)
class LessonType(StrEnum):
    LECTION = "ЛК"
    PRACTISE = "ПР"

    @classmethod
    def from_name(cls, name: str) -> Self:
        match name.strip():
            case "Лекция":
                return cls.LECTION
            case "Практика":
                return cls.PRACTISE

    @property
    def formatted(self) -> str:
        return self.value + "\t"
