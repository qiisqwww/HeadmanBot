from datetime import time
from typing import Annotated, Any

from pydantic import AfterValidator, BaseModel

from src.modules.utils.schedule_api.domain import Weekday

__all__ = [
    "MireaScheduleSchema",
]


class Period(BaseModel):
    id: int
    year_start: int
    year_end: int
    semester: int


class Institute(BaseModel):
    id: int
    short_name: str
    name: str


class Degree(BaseModel):
    id: int
    name: str


class LessonType(BaseModel):
    id: int
    name: str


class Discipline(BaseModel):
    id: int
    name: str


class Teacher(BaseModel):
    id: int
    name: str


class Campus(BaseModel):
    id: int
    name: str
    short_name: str


class Room(BaseModel):
    id: int
    campus_id: int
    name: str
    campus: Campus


class Call(BaseModel):
    id: int
    num: int
    time_start: time
    time_end: time


class Lesson(BaseModel):
    id: int
    lesson_type: LessonType
    discipline: Discipline
    teachers: list[Teacher]
    room: Room
    calls: Call
    weekday: Annotated[Weekday, AfterValidator(lambda weekday: Weekday(weekday - 1))]
    subgroup: Any
    weeks: list[int]


class MireaScheduleSchema(BaseModel):
    id: int
    name: str
    period: Period
    institute: Institute
    degree: Degree
    lessons: list[Lesson]
