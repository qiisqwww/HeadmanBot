from dataclasses import dataclass
from datetime import time
from typing import Any, Mapping, Self

from src.dto.dto import DTO

__all__ = [
    "Lesson",
]


@dataclass(slots=True)
class Lesson(DTO):
    id: int
    group_id: int
    discipline: str
    start_time: time
    weekday: int

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            id=data["id"],
            group_id=data["group_id"],
            discipline=data["discipline"],
            start_time=data["start_time"],
            weekday=data["weekday"],
        )

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Lesson):
            return NotImplemented

        return self.start_time > other.start_time
