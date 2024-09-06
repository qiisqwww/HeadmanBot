from datetime import date, datetime, timezone
from typing import Final, NoReturn
from zoneinfo import ZoneInfo

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule, UniTimezone, LessonType
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry
from src.modules.utils.schedule_api.infrastructure.exceptions import (
    FailedToCheckGroupExistenceError,
    ParsingScheduleAPIResponseError,
    UnexpectedScheduleDataError
)

__all__ = [
    "NSTUScheduleAPI"
]


class NSTUScheduleAPI(ScheduleAPI):
    _GROUP_SCHEDULE_URL: Final[str] = \
        "https://www.nstu.ru/studies/schedule/schedule_classes/schedule?group={group_name}&print=true"
    _SUNDAY: Final[int] = 6
    _FIRST_WEEK = 36

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        try:
            all_schedule_bin = await self._fetch_all_schedule(group_name)
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
        day = day or datetime.now(tz=ZoneInfo(UniTimezone.NSTU_TZ))
        current_week = day.isocalendar().week - self._FIRST_WEEK + 1

        today = day.weekday()
        if today == self._SUNDAY:
            return []

        try:
            all_schedule_bin = await self._fetch_all_schedule(group_name)
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

        schedule = []
        # Итерируемся только по дочерним объектам, которые являются объектами класса Tag
        for lesson in [item for item in list(today_schedule_soup.children) if isinstance(item, Tag)]:
            lessons_this_time = lesson.find_all("div", class_="schedule__table-row")  # На это время (в разные недели)
            if all(lesson_this_time.text.strip() == "" for lesson_this_time in lessons_this_time):
                continue

            # Необходимо определить, какая именно пара будет проходить в это время на этой неделе
            lesson_this_time_info = None
            for applicant_lesson_this_time in lessons_this_time:
                applicant_lesson_infos = [ch for ch in applicant_lesson_this_time.children if isinstance(ch, Tag)][0]
                applicant_lesson_info = [lesson_info.text for lesson_info in applicant_lesson_infos.children][1]

                filtered_applicant_info = []
                for l in applicant_lesson_info.split("\n"):
                    if len(l.replace("\t", "")) > 0:
                        filtered_applicant_info.append(l.replace("\t", ""))

                if len(filtered_applicant_info) > 5:
                    err_msg = (
                        "Got an unexpected count of arguments for lesson from NSTU API (or the format "
                        "data is stored in was changed"
                    )
                    raise UnexpectedScheduleDataError(err_msg)

                if all(stamp not in filtered_applicant_info[0].lower() for stamp in [
                    "недели",
                    "по чётным",
                    "по нечётным"
                ]):
                    lesson_this_time_info = filtered_applicant_info
                    break

                if "недели" in filtered_applicant_info[0].lower():
                    weeks = filtered_applicant_info[0].split(" ")[1:]
                    if str(current_week) in weeks:
                        lesson_this_time_info = filtered_applicant_info[1:]
                        break
                if "по чётным" in filtered_applicant_info[0].lower():
                    lesson_this_time_info = filtered_applicant_info[1:] if current_week % 2 == 0 else None
                elif "по нечётным" in filtered_applicant_info[0].lower():
                    lesson_this_time_info = filtered_applicant_info[1:] if current_week % 2 != 0 else None

            if lesson_this_time_info is None:
                continue

            # Необходимо достать время начала пары
            start_time = (datetime.strptime(
                lesson.find("div", class_="schedule__table-time").text.split("-")[0],
                '%H:%M'
            ) - datetime.now(tz=ZoneInfo(UniTimezone.NSTU_TZ)).utcoffset()).time()

            lesson_type = LessonType.from_name(lesson_this_time_info[-2])
            lesson_name = lesson_type.formatted + lesson_this_time_info[0].split("·")[0]

            schedule.append(Schedule(
                lesson_name=lesson_name,
                start_time=start_time,
                classroom=lesson_this_time_info[-1].strip()
            ))

        return schedule

    @aiohttp_retry(attempts=3)
    async def _fetch_all_schedule(self, group_name: str) -> str:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as session:
            response = await session.get(self._GROUP_SCHEDULE_URL.format(group_name=group_name))
            response_payload = await response.text()
        return response_payload
