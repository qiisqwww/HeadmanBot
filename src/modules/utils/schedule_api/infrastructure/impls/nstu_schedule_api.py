from datetime import date, datetime
from typing import Final, NoReturn
from zoneinfo import ZoneInfo

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from src.modules.common.domain import UniversityAlias
from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule, UniTimezone
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry
from src.modules.utils.schedule_api.infrastructure.exceptions import (
    FailedToCheckGroupExistenceError,
    ParsingScheduleAPIResponseError,
)

__all__ = [
    "NSTUScheduleAPI"
]


class NSTUScheduleAPI(ScheduleAPI):
    _GROUP_SCHEDULE_URL: Final[str] = \
        "https://www.nstu.ru/studies/schedule/schedule_classes/schedule?group={group_name}&print=true"
    _SUNDAY: Final[int] = 6

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        try:
            all_schedule_bin = await self._fetch_all_schedule()
        except Exception as e:
            err_msg = "Failed to fetch index page for schedule using NSTU API."
            raise FailedToCheckGroupExistenceError(err_msg) from e

        try:
            all_schedule_soup = BeautifulSoup(all_schedule_bin, "html.parser")
            info_about_lessons = all_schedule_soup.find(
                "div",
                {"class": "schedule__table-body"}).findAll(
                "div",
                {"class": "schedule__table-row"})
        except Exception as e:
            err_msg = "Failed to parse index page for schedule using NSTU API."
            raise ParsingScheduleAPIResponseError(err_msg) from e

        return len(info_about_lessons) != 0

    async def fetch_schedule(self, group_name: str, day: date | None = None) -> list[Schedule] | NoReturn:
        day = day or datetime.now(tz=ZoneInfo(UniTimezone.NSTU_TZ)).date()

        today = day.weekday()
        if today == self._SUNDAY:
            return []

        try:
            all_schedule_bin = await self._fetch_all_schedule()
        except Exception as e:
            err_msg = "Failed to fetch index page for schedule using NSTU API."
            raise FailedToCheckGroupExistenceError(err_msg) from e

        try:
            all_schedule_soup = BeautifulSoup(all_schedule_bin, "html.parser")
            week_schedule_soup = [day for day in all_schedule_soup.find(
                "div",
                {"class": "schedule__table-body"}).children if isinstance(day, Tag)]
        except Exception as e:
            err_msg = "Failed to parse index page for schedule using NSTU API."
            raise ParsingScheduleAPIResponseError(err_msg) from e

        today_schedule_soup = [item for item in list(week_schedule_soup[today].children) if isinstance(item, Tag)][1]

    @aiohttp_retry(attempts=3)
    async def _fetch_all_schedule(self) -> str:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as session:
            response = await session.get(self._GROUP_SCHEDULE_URL)
            response_payload = await response.text()
        return response_payload
