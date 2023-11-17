import re
from datetime import datetime, time

from bs4 import BeautifulSoup, Tag
from httpx import AsyncClient

from src.dto import Schedule
from src.enums.weekday import Weekday

from .schedule_api_interface import IScheduleAPI

__all__ = [
    "BmstuScheduleApi",
]


class BmstuScheduleApi(IScheduleAPI):
    _ALL_SCHEDULE_URL: str = "https://lks.bmstu.ru/schedule/list"

    async def group_exists(self, group_name: str) -> bool:
        soup = await self._fetch_all_schedule_soup()
        group_tags = self._parse_group_tags_soup(soup)
        group_names = [tag.text.strip() for tag in group_tags]
        return group_name in group_names

    async def fetch_schedule(self, group_name: str, weekday: Weekday | None = None) -> list[Schedule]:
        if weekday is None:
            weekday = Weekday(datetime.today().weekday())

        if weekday == Weekday.SUNDAY:
            return []

        schedule_soup = await self._fetch_schedule_soup(group_name)
        today_schedule = self._get_today_schedule_table(weekday, schedule_soup)
        is_zn = self._is_zn(schedule_soup)

        rows: list[Tag] = today_schedule.find_all("tr")[2:]
        rows = self._filter_empty_rows(rows)

        return self._parse_schedule(rows, is_zn)

    def _parse_row(self, row: Tag, is_zn: bool) -> Schedule | None:
        cols = row.find_all("td")
        time_duration = cols[0].text

        if is_zn and len(cols) == 3:
            if cols[2].span is None:
                return None
            lesson_name = cols[2].span.text
        elif not is_zn and len(cols) == 3:
            if cols[1].span is None:
                return None
            lesson_name = cols[1].span.text
        else:
            lesson_name = cols[1].span.text

        start_time = time.fromisoformat(time_duration.split("-")[0].strip())

        return Schedule(lesson_name, start_time)

    def _parse_schedule(self, rows: list[Tag], is_zn: bool) -> list[Schedule]:
        res = []
        for row in rows:
            row_schedule = self._parse_row(row, is_zn)
            if row_schedule is not None:
                res.append(row_schedule)

        return res

    def _is_zn(self, schedule_soup: BeautifulSoup) -> bool:
        page_header = schedule_soup.find(class_="page-header")
        tag_with_zn_value = page_header.h4.i
        *_, zn_value = tag_with_zn_value.text.split()
        return zn_value == "знаменатель"

    def _filter_empty_rows(self, schedule_table: list[Tag]) -> list[Tag]:
        result = []
        for row in schedule_table:
            cols = row.find_all("td")
            is_empty = True

            for i in range(1, len(cols)):
                if cols[i].text.strip():
                    is_empty = False

            if not is_empty:
                result.append(row)

        return result

    async def _fetch_all_schedule_soup(self) -> BeautifulSoup:
        async with AsyncClient() as client:
            response = await client.get(self._ALL_SCHEDULE_URL)

        return BeautifulSoup(response.text, "html.parser")

    async def _fetch_schedule_soup(self, group_name: str) -> BeautifulSoup:
        soup = await self._fetch_all_schedule_soup()
        group_tags = self._parse_group_tags_soup(soup)

        group_schedule_url = ""
        for tag in group_tags:
            if tag.text.strip() == group_name:
                group_schedule_url = tag.attrs["href"]

        async with AsyncClient() as client:
            response = await client.get(f"https://lks.bmstu.ru{group_schedule_url}")

        return BeautifulSoup(response.text, "html.parser")

    def _parse_group_tags_soup(self, soup: BeautifulSoup) -> list[Tag]:
        group_pat = re.compile("/schedule/*+")
        return soup.find_all(href=group_pat)

    def _get_today_schedule_table(self, weekday: Weekday, schedule_soup: BeautifulSoup) -> Tag:
        day_schedule = schedule_soup.find_all(class_="col-lg-6 d-none d-md-block")[weekday]
        return day_schedule.table.tbody
