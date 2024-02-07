import re
from datetime import date, datetime
from typing import Final, final
from zoneinfo import ZoneInfo

import recurring_ical_events
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from icalendar import Calendar, Event

from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry

__all__ = [
    "BmstuScheduleApi",
]


@final
class BmstuScheduleApi(ScheduleAPI):
    _ALL_SCHEDULE_URL: Final[str] = "https://lks.bmstu.ru/schedule/list"
    _SUNDAY: Final[int] = 6

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool:
        soup = await self._fetch_all_schedule_soup()
        group_tags = self._parse_group_tags_soup(soup)
        group_names = [tag.text.strip() for tag in group_tags]
        return group_name in group_names

    async def fetch_schedule(self, group_name: str, day: date | None = None) -> list[Schedule]:
        day = day or datetime.now(tz=ZoneInfo("UTC")).date()

        if day.weekday() == self._SUNDAY:
            return []

        soup = await self._fetch_all_schedule_soup()
        isc_url = self._parse_isc_url(soup, group_name)
        isc_file = await self._fetch_isc(isc_url)

        calendar: Calendar = Calendar.from_ical(isc_file)
        events: list[Event] = recurring_ical_events.of(calendar).at(day) # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
        return [
            Schedule(
                lesson_name=str(event["SUMMARY"]), # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
                start_time=event["DTSTART"].dt.timetz(), # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
            )
            for event in events
        ]

    def _parse_isc_url(self, page: BeautifulSoup, group_name: str) -> str:
        group_tags = self._parse_group_tags_soup(page)

        group_schedule_url = ""
        for tag in group_tags:
            if tag.text.strip() == group_name:
                group_schedule_url = tag.attrs["href"]
        return  f"https://lks.bmstu.ru{group_schedule_url}.ics"

    @aiohttp_retry(attempts=3)
    async def _fetch_all_schedule_soup(self) -> BeautifulSoup:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as session, session.get(self._ALL_SCHEDULE_URL) as response:
            response_payload = await response.text()
        return BeautifulSoup(response_payload, "html.parser")

    @aiohttp_retry(attempts=3)
    async def _fetch_isc(self, url: str) -> str:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as client, client.get(url) as response:
            payload: str = await response.text()
        return payload

    def _parse_group_tags_soup(self, soup: BeautifulSoup) -> list[Tag]:
        group_pat = re.compile("/schedule/*")
        return soup.find_all(href=group_pat)
