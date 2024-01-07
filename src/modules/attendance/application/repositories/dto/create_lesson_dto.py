from dataclasses import dataclass
from datetime import time

from src.dto.models import GroupId

__all__ = [
    "CreateLessonDTO",
]


@dataclass(frozen=True, slots=True)
class CreateLessonDTO:
    name: str
    group_id: GroupId
    start_time: time
