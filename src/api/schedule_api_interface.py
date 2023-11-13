from abc import ABC, abstractmethod

from src.dto import Schedule
from src.enums import Weekday

__all__ = [
    "IScheduleAPI",
]


class IScheduleAPI(ABC):
    @abstractmethod
    async def group_exists(self, group_name: str) -> bool:
        ...

    @abstractmethod
    async def fetch_schedule(self, group_name: str, weekday: Weekday | None = None) -> list[Schedule]:
        ...
