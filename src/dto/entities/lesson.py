from dataclasses import dataclass
from datetime import time
from typing import NewType

from .group import GroupId

__all__ = [
    "Lesson",
    "LessonId",
]

LessonId = NewType("LessonId", int)


@dataclass(slots=True, frozen=True)
class Lesson:
    id: LessonId
    group_id: GroupId
    name: str
    start_time: time
