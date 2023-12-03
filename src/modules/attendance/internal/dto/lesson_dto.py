from dataclasses import dataclass
from datetime import time
from typing import Any

from src.kernel.base import DTO

__all__ = [
    "LessonDTO",
]


@dataclass(slots=True, frozen=True)
class LessonDTO(DTO):
    id: int
    group_id: int
    name: str
    start_time: time

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, LessonDTO):
            return NotImplemented

        return self.start_time > other.start_time

    def __str__(self) -> str:
        return f"{self.name} {self.start_time.strftime('%H:%M')}"

    @property
    def str_start_time(self) -> str:
        return self.start_time.strftime("%H:%M")
