from injector import inject
from src.modules.utils.schedule_api.application import ScheduleAPI

from src.common import UseCase
from src.dto.enums.university_alias import UniversityAlias

__all__ = [
    "CheckGroupExistsInUniQuery",
]


class CheckGroupExistsInUniQuery(UseCase):
    _schedule_api_impl: type[ScheduleAPI]

    @inject
    def __init__(self, schedule_api_impl: type[ScheduleAPI]) -> None:
        self._schedule_api_impl = schedule_api_impl

    async def execute(self, group_name: str, university_alias: UniversityAlias) -> bool:
        schedule_api = self._schedule_api_impl(university_alias)

        return await schedule_api.group_exists(group_name)
