from typing import Self
from enum import StrEnum, verify, UNIQUE

__all__ = [
    "BMSTULessonType",
]


@verify(UNIQUE)
class BMSTULessonType(StrEnum):
    LECTION = "ЛК"
    PRACTISE = "ПР"
    LABORATORY = "ЛБ"
    NOTHING = ""

    @classmethod
    def from_name(cls, name: str) -> Self:
        match name.strip():
            case "lection":
                return cls.LECTION
            case "seminar":
                return cls.PRACTISE
            case "DID NOT FOUND":  # TODO: fix this
                return cls.LABORATORY
            case _:
                return cls.NOTHING

    @property
    def formatted(self) -> str:
        if self.value:
            return self.value + "\t"
        return ""
