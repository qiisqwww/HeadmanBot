from datetime import date, datetime
from typing import Final, NoReturn
from zoneinfo import ZoneInfo

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule, UniTimezone, STULessonType
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry
from src.modules.utils.schedule_api.infrastructure.exceptions import (
    ParsingScheduleAPIResponseError,
    UnexpectedScheduleDataError,
    FailedToFetchScheduleError
)

__all__ = [
    "STUScheduleAPI"
]


class STUScheduleAPI(ScheduleAPI):
    _GROUP_SCHEDULE_URL: Final[str] = \
        ("http://www.stu.ru/education/raspisanie_table.php?group={group_id}&lecturer_oid=0&date_from={date_from}"
         "&cur_year={year}&_=1726056684017")
    _FIND_GROUP_ID_URL = \
        "http://www.stu.ru/education/raspisanie_groups.php?faculty=&group=&cur_year=2024&_=1726061460938"
    _SUNDAY: Final[int] = 6

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        try:
            all_groups_bin = await self._fetch_all_groups()
        except Exception as e:
            err_msg = "Failed to fetch index page for groups using STU API."
            raise FailedToFetchScheduleError(err_msg) from e

        try:
            group_id = await self._find_group_id(all_groups_bin, group_name)
        except Exception as e:
            err_msg = "Failed to parse index page for groups using STU API."
            raise ParsingScheduleAPIResponseError(err_msg) from e

        return group_id is not None

    async def fetch_schedule(self, group_name: str, day: date | None = None) -> list[Schedule] | NoReturn:
        day = day or datetime.now(tz=ZoneInfo(UniTimezone.STU_TZ))
        schedule_date = day.date() if isinstance(day, datetime) else day

        today = day.weekday()
        if today == self._SUNDAY:
            return []

        try:
            all_groups_bin = await self._fetch_all_groups()
        except Exception as e:
            err_msg = "Failed to fetch index page for groups using STU API."
            raise FailedToFetchScheduleError(err_msg) from e

        try:
            group_id = await self._find_group_id(all_groups_bin, group_name)
        except Exception as e:
            err_msg = "Failed to parse index page for groups using STU API."
            raise ParsingScheduleAPIResponseError(err_msg) from e

        try:
            all_schedule_bin = await self._fetch_all_schedule(group_id, str(schedule_date), day.year)
        except Exception as e:
            err_msg = "Failed to fetch index page for schedule using STU API."
            raise FailedToFetchScheduleError(err_msg) from e

        try:
            all_schedule_soup = BeautifulSoup(all_schedule_bin, "html.parser")
            schedule_table = all_schedule_soup.find_all("tr", {"style": True})
        except Exception as e:
            err_msg = "Failed to parse index page for schedule using STU API."
            raise ParsingScheduleAPIResponseError(err_msg) from e

        try:
            schedule = []
            for line in schedule_table:
                date_tag = line.find("td", attrs={"rowspan": True})
                if date_tag:
                    schedule_date = ".".join(str(schedule_date).split("-")[::-1])
                    if schedule_date not in date_tag.text:
                        break

                index = 1 if date_tag else 0
                lesson_data = line.find_all("td")

                try:
                    start_time = (datetime.strptime(lesson_data[index].text.split("-")[0].rstrip(), '%H:%M')
                                  - datetime.now(tz=ZoneInfo(UniTimezone.STU_TZ)).utcoffset()).time()
                    lesson_name = (STULessonType.from_name(lesson_data[index + 2].text).formatted
                                   + lesson_data[index + 1].text)
                    classroom = lesson_data[index + 3].text
                except Exception as e:
                    err_msg = (
                        "Got an unexpected count of arguments for lesson from STU API (or the format "
                        "data is stored in was changed"
                    )
                    raise UnexpectedScheduleDataError(err_msg) from e

                schedule.append(Schedule(lesson_name, start_time, classroom))
        except Exception as e:
            err_msg = "Exception raised while parsing schedule data using STU API."
            raise ParsingScheduleAPIResponseError(err_msg) from e

        return schedule

    @aiohttp_retry(attempts=3)
    async def _fetch_all_schedule(self, group_id: str, date_from: str, year: int) -> str:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as session:
            response = await session.get(self._GROUP_SCHEDULE_URL.format(
                group_id=group_id,
                date_from=date_from,
                year=year
            ))
            response_payload = await response.text()

        return response_payload

    @aiohttp_retry(attempts=3)
    async def _fetch_all_groups(self) -> str | None:
        async with ClientSession() as session:
            response = await session.get(self._FIND_GROUP_ID_URL)
            response_payload = await response.text()

        return response_payload

    @staticmethod
    async def _find_group_id(response_payload: str, group_name: str) -> str | None:
        group_founder_soup = BeautifulSoup(response_payload, "html.parser")
        groups = group_founder_soup.find(
            "select",
            {"id": "group"}
        ).find_all("option", {"data-faculty": True})

        group_id, previous_group_id, previous_text = None, None, None
        for group in groups:
            if group_name == group.text.strip():
                group_id = group.get("value")
            if previous_text and group_name == previous_text[:(len(previous_text) - len(group.text))].strip():
                group_id = previous_group_id
                break
            previous_text = group.text
            previous_group_id = group.get("value")

        return group_id
