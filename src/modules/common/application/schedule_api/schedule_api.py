from abc import ABC, abstractmethod

from src.modules.common.domain import UniversityAlias

from .schedule import Schedule
from .weekday import Weekday

__all__ = [
    "ScheduleAPI",
]


class ScheduleAPI(ABC):
    @abstractmethod
    def __init__(self, university_alias: UniversityAlias) -> None:
        ...

    @abstractmethod
    async def group_exists(self, group_name: str) -> bool:
        """Check group existence using university API."""

    @abstractmethod
    async def fetch_schedule(self, group_name: str, weekday: Weekday | None = None) -> list[Schedule]:
        """Fetch schedule for selected weekday or for today by default. Work in range of current week."""
