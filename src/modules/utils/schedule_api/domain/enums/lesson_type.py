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
    NOTHING = ""

    @classmethod
    def from_name(cls, name: str) -> Self:
        logger.error(name)
        match name.strip():
            case "Лекция":
                return cls.LECTION
            case "Практика":
                return cls.PRACTISE
            case _:
                return cls.NOTHING

    @property
    def formatted(self) -> str:
        if self.value:
            return self.value + "\t"
        return ""
