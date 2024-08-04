import re
from datetime import date, datetime, tzinfo
from typing import Final, final
from zoneinfo import ZoneInfo

import recurring_ical_events
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from icalendar import Calendar, Event

from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry
from src.modules.utils.schedule_api.infrastructure.exceptions import (
    FailedToCheckGroupExistenceError,
    FailedToFetchScheduleError,
    GroupNotFoundError,
    ParsingScheduleAPIResponseError,
)

__all__ = [
    "BmstuScheduleApi",
]


@final
class BmstuScheduleApi(ScheduleAPI):
    _ALL_SCHEDULE_URL: Final[str] = "https://lks.bmstu.ru/schedule/list"
    _SUNDAY: Final[int] = 6
    _API_TIMEZONE: Final[tzinfo] = ZoneInfo("UTC")

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool:
        """Returns true if group exists in BMSTU."""
        try:
            all_schedule_bin = await self._fetch_all_schedule()
        except Exception as e:
            err_msg = "Failed to fetch index page for schedule using BMSTU API."
            raise FailedToCheckGroupExistenceError(err_msg) from e

        try:
            all_schedule_soup = BeautifulSoup(all_schedule_bin, "html.parser")
            group_tags = self._parse_group_tags_soup(all_schedule_soup)
            group_names = [tag.text.strip() for tag in group_tags]
        except Exception as e:
            err_msg = "Failed to parse index page for schedule using BMSTU API."
            raise ParsingScheduleAPIResponseError(err_msg) from e

        return group_name in group_names

    async def fetch_schedule(
        self,
        group_name: str,
        day: date | None = None,
    ) -> list[Schedule]:
        """Returns schedule of BMSTU group if exists."""
        # day = day or datetime.now(tz=self._API_TIMEZONE).date()
        day = day or datetime.now(tz=ZoneInfo("Europe/Moscow")).date()

        if day.weekday() == self._SUNDAY:
            return []

        try:
            all_schedule_bin = await self._fetch_all_schedule()
        except Exception as e:
            err_msg = "Failed to fetch index page for schedule using BMSTU API."
            raise FailedToCheckGroupExistenceError(err_msg) from e

        try:
            all_schedule_soup = self._parse_html(all_schedule_bin)
            isc_url = self._parse_isc_url(all_schedule_soup, group_name)
        except Exception as e:
            err_msg = "Failed to parse isc file location from index schedule page using BMSTU API."
            raise ParsingScheduleAPIResponseError(err_msg) from e

        try:
            isc_file = await self._fetch_isc(isc_url)
        except Exception as e:
            err_msg = "Failed to fetch isc file with schedule using MIREA API."
            raise FailedToFetchScheduleError(err_msg) from e

        try:
            calendar: Calendar = Calendar.from_ical(
                isc_file,
            )  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            events: list[Event] = recurring_ical_events.of(calendar).at(
                day,
            )  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            schedule = [
                Schedule(
                    lesson_name=str(
                        event["SUMMARY"],
                    ),  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
                    start_time=event[
                        "DTSTART"
                    ].dt.timetz(),  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
                    classroom=str(event.get("LOCATION", "")),
                )
                for event in events
            ]
        except Exception as e:
            err_msg = "Failed to parse schedule from isc file using BMSTU API"
            raise ParsingScheduleAPIResponseError(err_msg) from e

        return schedule

    def _parse_html(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")

    def _parse_isc_url(self, page: BeautifulSoup, group_name: str) -> str:
        """Return url to download .ics schedule file of BMSTU group."""
        group_tags = self._parse_group_tags_soup(page)

        group_schedule_url = None
        for tag in group_tags:
            if tag.text.strip() == group_name:
                group_schedule_url = tag.attrs["href"]

        if group_schedule_url is None:
            err_msg = f"Failed to find location of isc file for group '{group_name}'"
            raise GroupNotFoundError(err_msg)

        return f"https://lks.bmstu.ru{group_schedule_url}.ics"

    @aiohttp_retry(attempts=3)
    async def _fetch_all_schedule(self) -> str:
        """Fetches index page for schedule using BMSTU API."""
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as session, session.get(
            self._ALL_SCHEDULE_URL,
        ) as response:
            response_payload: str = await response.text()
        return response_payload

    @aiohttp_retry(attempts=3)
    async def _fetch_isc(self, url: str) -> str:
        """Fetches isc file for BMSTU group."""
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as client, client.get(
            url,
        ) as response:
            payload: str = await response.text()
        return payload

    def _parse_group_tags_soup(self, soup: BeautifulSoup) -> list[Tag]:
        group_pat = re.compile("/schedule/*")
        return soup.find_all(href=group_pat)
