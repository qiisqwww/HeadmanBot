from datetime import date, datetime
from typing import Final, NoReturn
from zoneinfo import ZoneInfo

from aiohttp import ClientSession

from src.modules.utils.schedule_api.domain import Schedule, UniTimezone, Weekday, MIIKAIKLessonType
from src.modules.utils.schedule_api.infrastructure.aiohttp_retry import aiohttp_retry
from src.modules.utils.schedule_api.application import ScheduleAPI

__all__ = [
    "MIIGAIKScheduleAPI"
]


class MIIGAIKScheduleAPI(ScheduleAPI):
    _GROUP_DATA_URL: Final[str] = "https://study.miigaik.ru/api/v1/search/group?groupName={group_name}"
    _GROUP_SCHEDULE_URL: Final[str] = "https://study.miigaik.ru/api/v1/{current_week_schedule_link}"
    _SUNDAY: Final[int] = 6

    def __init__(self) -> None:
        ...

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        # Возвращает список со всеми группами, которые включают group_name
        # (их имена и ссылка на получение json с расписанием)
        all_groups_data = await self._fetch_all_groups_data(group_name)

        # Длина списка должна быть равна единице, иначе название группы неполное
        return len(all_groups_data) == 1 and all_groups_data[0].get("groupName", "") == group_name

    async def fetch_schedule(self, group_name: str, day: date | None = None) -> list[Schedule] | NoReturn:
        weekday = Weekday.today()
        weekday_str = weekday.russian_lowercase()

        current_week_schedule_link = await self._find_current_week_schedule_link(group_name)
        group_schedule = await self.fetch_schedule(current_week_schedule_link)

        if len(group_schedule) == 0:  # У группы нет пар на этой неделе
            return []

        group_day_schedule = group_schedule.get(weekday_str, None)
        if not group_day_schedule:  # В этот день недели нет пар
            return []

        schedule = []
        for lesson in group_day_schedule:
            start_time = (datetime.strptime(lesson["lessonStartTime"].text.split("-")[0].rstrip(), '%H:%M')
                          - datetime.now(tz=ZoneInfo(UniTimezone.MIIGAIK_TZ)).utcoffset()).time()

            schedule.append(Schedule(
                lesson_name=MIIKAIKLessonType.from_name(lesson["lessonType"]).formatted + lesson["disciplineName"],
                classroom=(lesson.get("classroomBuilding", "") + " " + lesson.get("classroomName", "")).strip(),
                start_time=start_time
            ))

        return schedule

    async def _find_current_week_schedule_link(self, group_name: str) -> str:
        all_groups_data = await self._fetch_all_groups_data(group_name)
        return all_groups_data[0].get("currentWeekScheduleLink")

    @aiohttp_retry(3)
    async def _fetch_all_groups_data(self, group_name: str) -> list:
        async with ClientSession() as session:
            response = await session.get(self._GROUP_DATA_URL.format(group_name=group_name))
            payload = await response.json()

        return payload

    @aiohttp_retry(3)
    async def _fetch_group_schedule(self, current_week_schedule_link: str) -> list:
        async with ClientSession() as session:
            response = await session.get(self._GROUP_SCHEDULE_URL.format(current_week_schedule_link))
            payload = await response.json()

            return payload.get("schedule", [])
