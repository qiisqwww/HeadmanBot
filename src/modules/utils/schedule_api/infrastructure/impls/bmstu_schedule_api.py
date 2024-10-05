from datetime import date, datetime, tzinfo
from typing import Any, Final, final
from zoneinfo import ZoneInfo

from aiohttp import ClientSession

from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import BMSTULessonType, Schedule, UniTimezone
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry
from src.modules.utils.schedule_api.infrastructure.exceptions import (
    FailedToCheckGroupExistenceError,
    FailedToFetchScheduleError,
    ParsingScheduleAPIResponseError,
)

__all__ = [
    "BMSTUScheduleAPI",
]


# TODO: rework errors for all API classes
@final
class BMSTUScheduleAPI(ScheduleAPI):
    _ALL_GROUPS_URL: Final[str] = "https://lks.bmstu.ru/lks-back/api/v1/structure"
    _GROUP_SCHEDULE_URL: Final[str] = "https://lks.bmstu.ru/lks-back/api/v1/schedules/groups/{group_uuid}/public"
    _FIRST_WEEK: Final[int] = 36
    _SUNDAY: Final[int] = 6
    _API_TIMEZONE: Final[tzinfo] = ZoneInfo("UTC")

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool:
        """Returns true if group exists in BMSTU.
        """
        try:
            all_schedule_json = await self._fetch_all_schedule()
        except Exception as e:
            err_msg = "Failed to fetch index page for schedule using BMSTU API."
            raise FailedToCheckGroupExistenceError(err_msg) from e

        return await self._get_group_data(all_schedule_json, group_name) is not None

    async def fetch_schedule(
        self,
        group_name: str,
        day: date | None = None,
    ) -> list[Schedule]:
        """Returns schedule of BMSTU group if exists.
        """
        day = day or datetime.now(tz=ZoneInfo(UniTimezone.BMSTU_TZ)).date()
        current_week = day.isocalendar().week - self._FIRST_WEEK + 1

        if day.weekday() == self._SUNDAY:
            return []

        try:
            all_schedule_json = await self._fetch_all_schedule()
        except Exception as e:
            err_msg = "Failed to fetch index page for schedule using BMSTU API."
            raise FailedToFetchScheduleError(err_msg) from e

        try:
            group_data = await self._get_group_data(all_schedule_json, group_name)
            group_schedule = (await self._fetch_group_schedule(group_data["uuid"]))["data"]
        except Exception as e:
            err_msg = "Failed to fetch group_schedule using group_data using BMSTU API."
            raise ParsingScheduleAPIResponseError(err_msg) from e

        try:
            schedule = []
            for lesson in group_schedule["schedule"]:
                if lesson["day"] != day.weekday() + 1:
                    continue
                if lesson["week"] != "all":
                    week_parity = current_week % 2
                    if week_parity == 0 and lesson["week"] == "ch" or week_parity == 1 and lesson["week"] == "zn":
                        continue

                lesson_name = (BMSTULessonType.from_name(lesson.get("discipline", {}).get("actType", "")).formatted +
                               (lesson.get("discipline", {}).get("fullName", "") if lesson.get("discipline", {})
                                .get("fullName", "") else ""))

                start_time = ((datetime.strptime(
                    lesson["startTime"],
                    "%H:%M",
                )) - datetime.now(tz=ZoneInfo(UniTimezone.BMSTU_TZ)).utcoffset()).time()

                classroom = ""
                if lesson["audiences"]:
                    classroom = lesson["audiences"][0].get("name", "")
                print(classroom)

                schedule.append(Schedule(
                    lesson_name=lesson_name,
                    start_time=start_time,
                    classroom=classroom,
                ))
        except Exception as e:
            err_msg = "Failed to parse schedule from json file using BMSTU API"
            raise ParsingScheduleAPIResponseError(err_msg) from e

        return schedule

    @aiohttp_retry(attempts=3)
    async def _fetch_all_schedule(self) -> dict[str, Any]:
        """Fetches index page for schedule using BMSTU API.
        """
        async with ClientSession() as session, session.get(self._ALL_GROUPS_URL) as response:
            response_payload: dict[str, Any] = await response.json()

        return response_payload

    @aiohttp_retry(3)
    async def _fetch_group_schedule(self, group_uuid: str) -> dict[str, Any]:
        """Fetches group schedule using BMSTU API.
        """
        async with (ClientSession() as session, session.get(
                self._GROUP_SCHEDULE_URL.format(group_uuid=group_uuid)) as response):
            response_payload: dict[str, Any] = await response.json()

        return response_payload

    @staticmethod
    async def _get_group_data(all_schedule_json: dict, group_name: str) -> dict | None:  # TODO: Refactor this shit
        """Returns list of group's schedule from json.
        """
        for universities in all_schedule_json["data"]["children"]:
            for institutes in universities["children"]:
                for direction in institutes["children"]:
                    for course in direction["children"]:
                        for group in course["children"]:
                            if group["abbr"] == group_name:
                                return group

        return None

