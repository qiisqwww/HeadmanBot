from abc import ABC, abstractmethod

from .dto import Schedule
from .enums import Weekday

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
