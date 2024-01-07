from dataclasses import dataclass

from src.domain.edu_info.models.group import Group
from src.kernel import Model

from .lesson import Lesson

__all__ = [
    "Schedule",
]


@dataclass(slots=True)
class Schedule(Model):
    group: Group
    lessons: list[Lesson]

    def __post_init__(self) -> None:
        self.lessons.sort()
