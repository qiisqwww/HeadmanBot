from abc import ABC, abstractmethod
from datetime import date, tzinfo
from typing import Final, NoReturn
from zoneinfo import ZoneInfo

from aiohttp import ClientTimeout

from src.modules.common.domain import UniversityAlias
from src.modules.utils.schedule_api.domain import Schedule

__all__ = [
    "ScheduleAPI",
]


class ScheduleAPI(ABC):
    _RESULT_TIMEZONE: Final[tzinfo] = ZoneInfo("UTC")
    _REQUEST_TIMEOUT: Final[ClientTimeout] = ClientTimeout(10.0)

    @abstractmethod
    def __init__(self, university_alias: UniversityAlias) -> None:
        ...

    @abstractmethod
    async def group_exists(self, group_name: str) -> bool | NoReturn:
        """Check group existence using university API."""

    @abstractmethod
    async def fetch_schedule(self, group_name: str, day: date | None = None) -> list[Schedule] | NoReturn:
        """Fetch schedule for selected weekday or for today by default. Work in range of current week."""
