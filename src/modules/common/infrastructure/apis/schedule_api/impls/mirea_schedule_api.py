from datetime import datetime, time, timedelta
from typing import final

from httpx import AsyncClient

from src.modules.common.application.schedule_api import Schedule, ScheduleAPI, Weekday
from src.modules.common.infrastructure import DEBUG
from src.modules.common.infrastructure.retry import retry

from .mirea_schedule_schema import Lesson, MireaScheduleSchema

__all__ = [
    "MireaScheduleApi",
]


@final
class MireaScheduleApi(ScheduleAPI):
    _URL: str = "https://timetable.mirea.ru/api/groups/name/{group_name}"
    _CURRENT_SEMESTR_START: datetime = datetime(year=2023, month=8, day=28)

    def __init__(self) -> None:
        ...

    async def fetch_schedule(self, group_name: str, weekday: Weekday | None = None) -> list[Schedule]:
        weekday = weekday or Weekday.today()

        json_schedule = await self._get_schedule_json(group_name)
        mirea_schedule = MireaScheduleSchema.model_validate_json(json_schedule)
        schedule = self._extract_day_schedule(mirea_schedule, weekday)

        if not schedule and DEBUG:
            return [
                Schedule("Физическая культура и спорт", time.fromisoformat("12:00")),
                Schedule("Математический анализ", time.fromisoformat("15:40")),
                Schedule("Аналитическая геометрия", time.fromisoformat("17:25")),
            ]

        return schedule

    @retry(attempts=3)
    async def group_exists(self, group_name: str) -> bool:
        async with AsyncClient() as client:
            response = await client.get(self._URL.format(group_name=group_name))
            return "errors" not in response.json()

    @retry(attempts=3)
    async def _get_schedule_json(self, group_name: str) -> bytes:
        async with AsyncClient() as client:
            response = await client.get(self._URL.format(group_name=group_name))
            return response.read()

    def _get_week_num(self, weekday: Weekday) -> int:
        today = datetime.today()
        week_start = today - timedelta(days=today.weekday())
        current_day = week_start + timedelta(days=weekday)
        return (current_day - self._CURRENT_SEMESTR_START).days // 7 + 1

    def _schedule_from_lesson(self, lesson: Lesson) -> Schedule:
        return Schedule(
            lesson_name=lesson.discipline.name,
            start_time=lesson.calls.time_start,
        )

    def _extract_day_schedule(self, mirea_schedule: MireaScheduleSchema, weekday: Weekday) -> list[Schedule]:
        weeknum = self._get_week_num(weekday)
        return [
            self._schedule_from_lesson(lesson)
            for lesson in mirea_schedule.lessons
            if lesson.weekday == weekday and weeknum in lesson.weeks
        ]
