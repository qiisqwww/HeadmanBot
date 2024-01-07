from datetime import datetime, time, timedelta
from typing import Any, Iterable

from httpx import AsyncClient

from src.modules.common.application.schedule_api import Schedule, ScheduleAPI, Weekday
from src.modules.common.infrastructure.retry import retry

__all__ = [
    "MireaScheduleApi",
]


class MireaScheduleApi(ScheduleAPI):
    _URL: str = "https://timetable.mirea.ru/api/groups/name/{group_name}"
    _MAX_LESSON_NAME_LEN: int = 16
    _CURRENT_SEMESTR_START: datetime = datetime(year=2023, month=8, day=28)

    def __init__(self) -> None:
        ...

    async def fetch_schedule(self, group_name: str, weekday: Weekday | None = None) -> list[Schedule]:
        """By default return today schedule."""
        weekday = weekday or Weekday(datetime.today().weekday())
        week_start = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
        day = week_start + timedelta(days=float(weekday))

        json_schedule = await self._get_json(group_name)
        parsed_schedule = self._parse_schedule(json_schedule, day)

        return [Schedule(name, time.fromisoformat(start_time)) for name, start_time in parsed_schedule]

    @retry(attempts=3)
    async def group_exists(self, group_name: str) -> bool:
        async with AsyncClient() as client:
            response = await client.get(self._URL.format(group_name=group_name))
            return "errors" not in response.json()

    @retry(attempts=3)
    async def _get_json(self, group_name: str) -> dict[str, Any]:
        async with AsyncClient() as client:
            response = await client.get(self._URL.format(group_name=group_name))
            return response.json()

    def _parse_lesson(self, lesson: dict) -> tuple[str, str]:
        lesson_name: str = lesson["discipline"]["name"]
        start_time: str = lesson["calls"]["time_start"]
        return (lesson_name, start_time)

    def _get_lessons_by_day(self, lessons: Iterable, weekday: int) -> filter:
        return filter(lambda lesson: lesson["weekday"] == weekday, lessons)

    def _get_lessons_by_week(self, lessons: Iterable, week_num: int) -> filter:
        return filter(lambda lesson: week_num in lesson["weeks"], lessons)

    def _get_week_num(self, day: datetime) -> int:
        return (day - self._CURRENT_SEMESTR_START).days // 7 + 1

    def _parse_schedule(self, json_schedule: dict[str, Any], day: datetime) -> list[tuple[str, str]]:
        weekday = day.weekday() + 1
        parsed_lessons = []
        lessons = self._get_lessons_by_day(json_schedule["lessons"], weekday)
        lessons = self._get_lessons_by_week(lessons, self._get_week_num(day))

        for lesson in lessons:
            parsed_lessons.append(self._parse_lesson(lesson))

        parsed_lessons = list(set(parsed_lessons))
        parsed_lessons.sort(key=lambda el: time.fromisoformat(el[1]))

        return parsed_lessons
