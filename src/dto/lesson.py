from dataclasses import dataclass
from datetime import time
from typing import Any, NewType

from .dto import DTO
from .group import GroupId

__all__ = [
    "Lesson",
    "LessonId",
]


LessonId = NewType("LessonId", int)


@dataclass(slots=True, frozen=True)
class Lesson(DTO):
    id: LessonId
    group_id: GroupId
    name: str
    start_time: time

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Lesson):
            return NotImplemented

        return self.start_time > other.start_time

    def __str__(self) -> str:
        return f"{self.name} {self.start_time.strftime('%H:%M')}"

    @property
    def str_start_time(self) -> str:
        return self.start_time.strftime("%H:%M")
