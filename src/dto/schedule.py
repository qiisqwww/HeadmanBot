from dataclasses import dataclass
from datetime import time

__all__ = [
    "Schedule",
]


@dataclass(slots=True)
class Schedule:
    lesson_name: str
    start_time: time
