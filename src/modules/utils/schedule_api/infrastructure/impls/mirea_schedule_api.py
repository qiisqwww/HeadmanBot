from datetime import date, datetime, tzinfo
from typing import Final, NoReturn, final
from zoneinfo import ZoneInfo

import recurring_ical_events
from aiohttp import ClientSession
from icalendar import Calendar, Event
from pydantic import ValidationError

from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry
from src.modules.utils.schedule_api.infrastructure.exceptions import (
    FailedToCheckGroupExistenceError,
    FailedToFetchScheduleError,
    GroupNotFoundError,
    ParsingScheduleAPIResponseError,
)

from .mirea_isc_link_schema import MireaIscLinkSchema

__all__ = [
    "MireaScheduleApi",
]


@final
class MireaScheduleApi(ScheduleAPI):
    _FIND_URL: Final[
        str
    ] = "https://schedule-of.mirea.ru/schedule/api/search?match={group_name}"
    _API_TIMEZONE: Final[tzinfo] = ZoneInfo("Europe/Moscow")

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        try:
            isc_link_location_bin = await self._fetch_isc_link_location(group_name)
        except Exception as e:
            err_msg = "Failed to fetch json with isc file location using MIREA API."
            raise FailedToCheckGroupExistenceError(err_msg) from e

        try:
            isc_link_location = MireaIscLinkSchema.model_validate_json(
                isc_link_location_bin,
            )
        except ValidationError as e:
            err_msg = (
                "Failed to parse json which contains isc file location using MIREA API"
            )
            raise ParsingScheduleAPIResponseError(err_msg) from e

        return (
            len(isc_link_location.data) == 1
            and isc_link_location.data[0].targetTitle == group_name
        )

    async def fetch_schedule(
        self,
        group_name: str,
        day: date | None = None,
    ) -> list[Schedule] | NoReturn:
        day = day or datetime.now(tz=self._API_TIMEZONE).date()

        try:
            isc_link_location_bin = await self._fetch_isc_link_location(group_name)
        except Exception as e:
            err_msg = (
                "Failed to parse json which contains isc file location using MIREA API"
            )
            raise FailedToFetchScheduleError(err_msg) from e

        try:
            isc_link_location = MireaIscLinkSchema.model_validate_json(
                isc_link_location_bin,
            )
        except ValidationError as e:
            err_msg = (
                "Failed to parse json which contains isc file location using MIREA API"
            )
            raise ParsingScheduleAPIResponseError(err_msg) from e

        if (
            len(isc_link_location.data) != 1
            or isc_link_location.data[0].targetTitle != group_name
        ):
            err_msg = f"Failed to find group '{group_name}' using MIREA API for fetching schedule."
            raise GroupNotFoundError(err_msg)

        isc_url = isc_link_location.data[0].iCalLink

        try:
            isc_file = await self._fetch_isc(isc_url.unicode_string())
        except Exception as e:
            err_msg = "Failed to fetch isc file with schedule using MIREA API."
            raise FailedToFetchScheduleError(err_msg) from e

        try:
            calendar: Calendar = Calendar.from_ical(
                isc_file,
            )  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            schedule = self._parse_schedule_from_calendar(
                calendar,
                day,
            )  # pyright: ignore[reportUnknownArgumentType]
        except Exception as e:
            err_msg = "Failed to parse isc file with schedule from MIREA API."
            raise ParsingScheduleAPIResponseError(err_msg) from e

        return schedule

    def _parse_schedule_from_calendar(
        self,
        calendar: Calendar,
        day: date,
    ) -> list[Schedule]:
        events: list[Event] = recurring_ical_events.of(calendar).at(
            day,
        )  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
        schedule: list[Schedule] = []

        for event in events:
            start_datetime: datetime = event["DTSTART"].dt

            if not isinstance(start_datetime, datetime):
                continue

            start_time = start_datetime.astimezone(self._RESULT_TIMEZONE).timetz()
            schedule.append(
                Schedule(
                    lesson_name=str(event["SUMMARY"]),
                    start_time=start_time,
                    classroom=str(event.get("LOCATION", "")),
                ),
            )

        return schedule

    @aiohttp_retry(attempts=3)
    async def _fetch_isc_link_location(self, group_name: str) -> bytes:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as client, client.get(
            self._FIND_URL.format(group_name=group_name),
        ) as response:
            payload: bytes = await response.read()
        return payload

    @aiohttp_retry(attempts=3)
    async def _fetch_isc(self, url: str) -> str:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as client, client.get(
            url,
        ) as response:
            payload: str = await response.text()
        return payload
