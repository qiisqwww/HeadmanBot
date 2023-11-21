from dataclasses import dataclass
from datetime import time
from typing import Mapping, Self

__all__ = [
    "Schedule",
]


@dataclass(slots=True)
class Schedule:
    lesson_name: str
    start_time: time

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        raise NotImplementedError
