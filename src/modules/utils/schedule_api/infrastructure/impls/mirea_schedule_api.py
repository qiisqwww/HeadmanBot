from datetime import date, datetime, tzinfo
from typing import Final, NoReturn, final
from zoneinfo import ZoneInfo

import recurring_ical_events
from aiohttp import ClientSession
from icalendar import Calendar, Event

from src.modules.common.infrastructure.config import DEBUG
from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry

# from src.modules.utils.schedule_api.infrastructure.exceptions import (
#     FailedToCheckGroupExistenceError,
#     FailedToFetchScheduleError,
#     ParsingError,
# )
from .mirea_isc_link_schema import MireaIscLinkSchema

__all__ = [
    "MireaScheduleApi",
]


@final
class MireaScheduleApi(ScheduleAPI):
    _FIND_URL: Final[str] = "https://schedule-of.mirea.ru/schedule/api/search?match={group_name}"
    _API_TIMEZONE: Final[tzinfo] = ZoneInfo("Europe/Moscow")

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        isc_link_location_bin = await self._fetch_isc_link_location(group_name)
        isc_link_location = MireaIscLinkSchema.model_validate_json(isc_link_location_bin)

        if len(isc_link_location.data) == 1 and isc_link_location.data[0].targetTitle == group_name:
            return True
        return False

    async def fetch_schedule(self, group_name: str, day: date | None = None) -> list[Schedule] | NoReturn:
        day = day or datetime.now(tz=self._API_TIMEZONE).date()
        if DEBUG:
            day = date(year=2023, month=12, day=25)

        isc_link_location_bin = await self._fetch_isc_link_location(group_name)
        isc_link_location = MireaIscLinkSchema.model_validate_json(isc_link_location_bin)
        isc_url = isc_link_location.data[0].iCalLink

        isc_file = await self._fetch_isc(isc_url.unicode_string())
        calendar: Calendar = Calendar.from_ical(isc_file) # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        return self._parse_schedule_from_calendar(calendar, day) # pyright: ignore[reportUnknownArgumentType]

    def _parse_schedule_from_calendar(self, calendar: Calendar, day: date) -> list[Schedule]:
        events: list[Event] = recurring_ical_events.of(calendar).at(day) # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
        schedule: list[Schedule] = []

        for event in events:
            start_datetime: datetime = event["DTSTART"].dt
            start_time = start_datetime.astimezone(self._RESULT_TIMEZONE).timetz()
            schedule.append(Schedule(lesson_name=str(event["SUMMARY"]), start_time=start_time))

        return schedule


    @aiohttp_retry(attempts=3)
    async def _fetch_isc_link_location(self, group_name: str) -> bytes:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as client, client.get(self._FIND_URL.format(group_name=group_name)) as response:
            payload: bytes =  await response.read()
        return payload

    @aiohttp_retry(attempts=3)
    async def _fetch_isc(self, url: str) -> str:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as client, client.get(url) as response:
            payload: str = await response.text()
        return payload
