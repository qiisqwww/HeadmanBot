from dataclasses import dataclass
from datetime import time

__all__ = [
    "Lesson",
]


@dataclass(slots=True, frozen=True)
class Lesson:
    id: int
    group_id: int
    name: str
    start_time: time
