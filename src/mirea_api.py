from datetime import datetime, time
from typing import Any, Generator, Iterable

import requests

__all__ = [
    "MireaScheduleApi",
]


class MireaScheduleApi:
    _URL: str = "https://timetable.mirea.ru/api/groups/name/{group_name}"
    _MAX_LESSON_NAME_LEN: int = 16
    _CURRENT_SEMESTR_START: datetime = datetime(year=2023, month=8, day=28)

    def get_schedule(self, group_name: str, day: datetime | None = None) -> list[tuple[str, str]]:
        """By default return today schedule."""
        day = day or datetime.now()

        json_schedule = self._get_json(group_name)
        return self._parse_schedule(json_schedule, day)

    def group_exists(self, group_name: str) -> bool:
        response = requests.get(self._URL.format(group_name=group_name)).json()
        return "errors" not in response

    def _get_json(self, group_name: str) -> dict[str, Any]:
        return requests.get(self._URL.format(group_name=group_name)).json()

    def _remove_words(self, string: str, remove_words: int) -> str:
        words = string.split()
        words = words[: len(words) - remove_words]
        return " ".join(words)

    def _shrink_lesson_name(self, lesson_name: str) -> str:
        remove_words = 0

        shrinked_name = lesson_name
        while len(shrinked_name) > self._MAX_LESSON_NAME_LEN:
            shrinked_name = self._remove_words(lesson_name, remove_words)
            remove_words += 1

        if remove_words:
            shrinked_name += " ..."

        return shrinked_name

    def _clean_start_time(self, raw_start_time: str) -> str:
        """Transform date from '10:00:00' into '10:00' format."""
        clean_start_time, _ = raw_start_time.rsplit(":", 1)
        return clean_start_time

    def _parse_lesson(self, lesson: dict) -> tuple[str, str]:
        lesson_name: str = self._shrink_lesson_name(lesson["discipline"]["name"])
        start_time: str = self._clean_start_time(lesson["calls"]["time_start"])
        return (lesson_name, start_time)

    def _get_lessons_by_day(self, lessons: Iterable, weekday: int) -> Generator:
        return (lesson for lesson in lessons if lesson["weekday"] == weekday)

    def _get_lessons_by_week(self, lessons: Iterable, week_num: int) -> Generator:
        return (lesson for lesson in lessons if week_num in lesson["weeks"])

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
