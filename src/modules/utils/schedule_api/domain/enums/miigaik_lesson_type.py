from typing import Self
from enum import StrEnum, verify, UNIQUE

__all__ = [
    "MIIKAIKLessonType",
]


@verify(UNIQUE)
class MIIKAIKLessonType(StrEnum):
    LECTION = "ЛК"
    PRACTISE = "ПР"
    LABORATORY = "ЛБ"
    NOTHING = ""

    @classmethod
    def from_name(cls, name: str) -> Self:
        match name.strip():
            case "Лекционные занятия":
                return cls.LECTION
            case "Практические занятия":
                return cls.PRACTISE
            case "Лабораторные занятия":  # НЕ УВЕРЕН TODO
                return cls.LABORATORY
            case _:
                return cls.NOTHING

    @property
    def formatted(self) -> str:
        if self.value:
            return self.value + "\t"
        return ""
