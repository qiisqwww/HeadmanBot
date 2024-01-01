from dataclasses import dataclass

from src.dto.models.group import GroupId
from src.kernel import Model

from .lesson import Lesson

__all__ = [
    "Schedule",
]


@dataclass(slots=True)
class Schedule(Model):
    group_id: GroupId
    lessons: list[Lesson]

    def __post_init__(self) -> None:
        self.lessons.sort()
