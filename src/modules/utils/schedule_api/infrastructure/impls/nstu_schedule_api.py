from datetime import date, datetime, tzinfo
from typing import Final, NoReturn, final
from zoneinfo import ZoneInfo

import recurring_ical_events
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from icalendar import Calendar, Event

from src.modules.common.domain import UniversityAlias
from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry

__all__ = [
    "NSTUScheduleAPI"
]


class NSTUScheduleAPI(ScheduleAPI):
    _FIND_URL: Final[str] = \
        "https://www.nstu.ru/studies/schedule/schedule_classes/schedule?group={group_name}&print=true"

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        pass

    async def fetch_schedule(self, group_name: str, day: date | None = None) -> list[Schedule] | NoReturn:
        pass

