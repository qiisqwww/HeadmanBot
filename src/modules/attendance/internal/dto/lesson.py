from dataclasses import dataclass
from datetime import time
from typing import Any, Mapping, Self

__all__ = [
    "Lesson",
]


@dataclass(slots=True, frozen=True)
class Lesson:
    id: int
    group_id: int
    name: str
    start_time: time

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            id=data["id"],
            group_id=data["group_id"],
            name=data["name"],
            start_time=data["start_time"],
        )

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Lesson):
            return NotImplemented

        return self.start_time > other.start_time

    def __str__(self) -> str:
        return f"{self.name} {self.start_time.strftime('%H:%M')}"

    @property
    def str_start_time(self) -> str:
        return self.start_time.strftime("%H:%M")
