from src.application.common.apis.schedule_api import ScheduleAPI
from src.domain.edu_info import UniversityAlias

__all__ = [
    "CheckGroupExistsInUniQuery",
]


class CheckGroupExistsInUniQuery:
    _schedule_api_impl: type[ScheduleAPI]

    def __init__(self, schedule_api_impl: type[ScheduleAPI]) -> None:
        self._schedule_api_impl = schedule_api_impl

    async def execute(self, group_name: str, university_alias: UniversityAlias) -> bool:
        schedule_api = self._schedule_api_impl(university_alias)

        return await schedule_api.group_exists(group_name)
