from datetime import UTC, datetime
from typing import Final, NoReturn, final

import recurring_ical_events
from aiohttp import ClientSession
from icalendar import Calendar, Event

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

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        isc_link_location_bin = await self._fetch_isc_link_location(group_name)
        isc_link_location = MireaIscLinkSchema.model_validate_json(isc_link_location_bin)

        if len(isc_link_location.data) == 1 and isc_link_location.data[0].targetTitle == group_name:
            return True
        return False

    async def fetch_schedule(self, group_name: str, day: datetime | None = None) -> list[Schedule] | NoReturn:
        day = day or datetime.now(tz=UTC)

        isc_link_location_bin = await self._fetch_isc_link_location(group_name)
        isc_link_location = MireaIscLinkSchema.model_validate_json(isc_link_location_bin)
        isc_url = isc_link_location.data[0].iCalLink

        isc_file = await self._fetch_isc(isc_url.unicode_string())
        calendar: Calendar = Calendar.from_ical(isc_file) # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        return self._parse_schedule_from_calendar(calendar, day) # pyright: ignore[reportUnknownArgumentType]

    def _parse_schedule_from_calendar(self, calendar: Calendar, day: datetime) -> list[Schedule]:
        date = (day.year, day.month, day.day)
        events: list[Event] = recurring_ical_events.of(calendar).at(date) # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
        return [
            Schedule(
                lesson_name=str(event["SUMMARY"]), # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
                start_time=event["DTSTART"].dt.time(), # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
            )
            for event in events
        ]

    @aiohttp_retry(attempts=3)
    async def _fetch_isc_link_location(self, group_name: str) -> bytes:
        async with ClientSession() as client, client.get(self._FIND_URL.format(group_name=group_name)) as response:
            payload: bytes =  await response.read()
        return payload

    @aiohttp_retry(attempts=3)
    async def _fetch_isc(self, url: str) -> str:
        async with ClientSession() as client, client.get(url) as response:
            payload: str = await response.text()
        return payload
