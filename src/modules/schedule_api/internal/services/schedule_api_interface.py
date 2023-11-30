from abc import ABC, abstractmethod

from src.modules.schedule_api.internal.dto import Schedule
from src.modules.schedule_api.internal.enums import Weekday

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
