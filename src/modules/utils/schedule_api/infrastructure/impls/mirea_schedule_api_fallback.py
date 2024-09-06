from datetime import date, datetime, time
from typing import ClassVar, final, NoReturn
from itertools import batched
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
from aiohttp import ClientSession
from loguru import logger
import pandas as pd
import numpy as np

from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry



@final
class MireaScheduleApiFallback(ScheduleAPI):
    _INSTITUTS_CODES: ClassVar[dict[str, str]] = {
       "И": "IIT",
       "К": "III",
       "Р": "IRI",
       "Х": "ITKHT",
       "У": "ITU",
       "Э": "IPTIP",
       "Т": "IPTIP",
    }
    _URL: ClassVar[str] = "https://www.mirea.ru/schedule/"
    _classrooms_start: list[time] = [
        time(6, 00),
        time(7, 40),
        time(9, 40),
        time(11, 20),
        time(13, 20),
        time(15, 00),
        time(16, 40),
    ]
    _first_week: int = 36

    def __init__(self) -> None:
        ...

    async def fetch_schedule(self, group_name: str, day: date | None = None) -> list[Schedule] | NoReturn:
        now = datetime.now(tz=ZoneInfo("Europe/Moscow"))
        week_chetnost = (now.isocalendar().week - self._first_week) % 2
        weekday = now.weekday() if day is None else day.weekday()
        year = date.today().year % 100 - int(group_name[-2:]) + 1
        institute_name = self._get_institute_name(group_name) + "_" + str(year)
        page = await self._fetch_page()
        soup = BeautifulSoup(page, 'html.parser')

        links = list(filter(lambda l: "https://webservices.mirea.ru/upload/iblock" in l['href'], soup.find_all("a")))
        links = list(filter(lambda l: institute_name in l['href'], soup.find_all("a")))
        link = links[0]['href']

        excel_bin = await self._fetch_excel(link)

        data = pd.read_excel(excel_bin).transpose()
        schedule = []

        for i in range(len(data)):
            if group_name == list(data.iloc[i])[0]:
                lessons = list(batched(data.iloc[i][2:], 14))
                classrooms = list(batched(data.iloc[i + 3][2:], 14))
                classrooms_type = list(batched(data.iloc[i + 1][2:], 14))

                for j, pack in enumerate(batched(zip(lessons[weekday], classrooms_type[weekday], classrooms[weekday]), 2)):
                    if not isinstance(pack[week_chetnost][0], float):
                        schedule.append(Schedule(
                            lesson_name=pack[week_chetnost][1] + " " + pack[week_chetnost][0],
                            start_time=self._classrooms_start[j],
                            classroom=pack[week_chetnost][2],
                        ))

        return schedule

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        raise NotImplementedError

    def _get_institute_name(self, group_name: str) -> str:
        return self._INSTITUTS_CODES[group_name[0]]

    @aiohttp_retry(attempts=3)
    async def _fetch_page(self) -> str:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as client, client.get(
            self._URL,
        ) as response:
            payload: str = await response.text()
        return payload

    @aiohttp_retry(attempts=3)
    async def _fetch_excel(self, url: str) -> bytes:
        async with ClientSession(timeout=self._REQUEST_TIMEOUT) as client, client.get(
            url,
        ) as response:
            payload = await response.content.read()
        return payload

