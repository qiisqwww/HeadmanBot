from dataclasses import dataclass
from datetime import time
from typing import Any

__all__ = [
    "Lesson",
]


@dataclass(slots=True, frozen=True)
class Lesson:
    id: int
    group_id: int
    name: str
    start_time: time

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Lesson):
            return NotImplemented

        return self.start_time > other.start_time
