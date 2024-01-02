from abc import ABC, abstractmethod

from src.domain.edu_info import UniversityAlias

from .dto import Schedule
from .enums import Weekday

__all__ = [
    "ScheduleAPI",
]


class ScheduleAPI(ABC):
    @abstractmethod
    def __init__(self, university_alias: UniversityAlias) -> None:
        ...

    @abstractmethod
    async def group_exists(self, group_name: str) -> bool:
        ...

    @abstractmethod
    async def fetch_schedule(self, group_name: str, weekday: Weekday | None = None) -> list[Schedule]:
        ...
