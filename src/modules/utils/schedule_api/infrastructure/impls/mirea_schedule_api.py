from datetime import datetime, time, timedelta
from typing import NoReturn, final

from aiohttp import ClientError, ClientSession
from pydantic import ValidationError
from pytz import UTC

from src.modules.common.infrastructure import DEBUG
from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule, Weekday
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry
from src.modules.utils.schedule_api.infrastructure.exceptions import (
    FailedToCheckGroupExistenceError,
    FailedToFetchScheduleError,
    ParsingError,
)

from .mirea_schedule_schema import MireaScheduleSchema

__all__ = [
    "MireaScheduleApi",
]


@final
class MireaScheduleApi(ScheduleAPI):
    _URL: str = "https://timetable.mirea.ru/api/groups/name/{group_name}"
    _CURRENT_SEMESTR_START: datetime = datetime(year=2023, month=8, day=28, tzinfo=UTC)
    _HTTP_404_STATUS: int = 404

    def __init__(self) -> None:
        ...

    async def fetch_schedule(self, group_name: str, weekday: Weekday | None = None) -> list[Schedule] | NoReturn:
        weekday = weekday or Weekday.today()


        try:
            body = await self._fetch_api_response_body(group_name)
        except (TimeoutError, ClientError) as e:
            raise FailedToFetchScheduleError from e

        try:
            mirea_schedule = MireaScheduleSchema.model_validate_json(body)
        except ValidationError as e:
            raise ParsingError from e

        schedule = self._extract_day_schedule(mirea_schedule, weekday)

        if not schedule and DEBUG:
            return [
                Schedule("Физическая культура и спорт", time.fromisoformat("12:00")),
                Schedule("Математический анализ", time.fromisoformat("15:40")),
                Schedule("Аналитическая геометрия", time.fromisoformat("17:25")),
            ]

        return schedule

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        try:
            status = await self._fetch_api_response_status(group_name)
        except (TimeoutError, ClientError) as e:
            raise FailedToCheckGroupExistenceError from e

        return bool(status != self._HTTP_404_STATUS)

    @aiohttp_retry(attempts=3)
    async def _fetch_api_response_status(self, group_name: str) -> int:
        async with ClientSession() as session, session.get(self._URL.format(group_name=group_name)) as response:
            status: int = response.status
            return status

    @aiohttp_retry(attempts=3)
    async def _fetch_api_response_body(self, group_name: str) -> bytes:
        async with ClientSession() as session, session.get(self._URL.format(group_name=group_name)) as response:
            body: bytes = await response.read()
            return body

    def _get_week_num(self, weekday: Weekday) -> int:
        today = datetime.now(tz=UTC)
        week_start = today - timedelta(days=today.weekday())
        current_day = week_start + timedelta(days=weekday)
        return (current_day - self._CURRENT_SEMESTR_START).days // 7 + 1

    def _extract_day_schedule(self, mirea_schedule: MireaScheduleSchema, weekday: Weekday) -> list[Schedule]:
        weeknum = self._get_week_num(weekday)

        return [
            Schedule(
                lesson_name=lesson.discipline.name,
                start_time=lesson.calls.time_start,
            )
            for lesson in mirea_schedule.lessons
            if lesson.weekday == weekday and weeknum in lesson.weeks
        ]
