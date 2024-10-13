from datetime import date
from typing import final

from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule

from src.common.domain import UniversityAlias
from .impls import BMSTUScheduleAPI, MIREAScheduleAPI, NSTUScheduleAPI, STUScheduleAPI

__all__ = [
    "ScheduleApiImpl",
]


@final
class ScheduleApiImpl(ScheduleAPI):
    _api_impl: ScheduleAPI

    def __init__(self, university: UniversityAlias) -> None:
        match university:
            case UniversityAlias.MIREA:
                self._api_impl = MIREAScheduleAPI()
            case UniversityAlias.BMSTU:
                self._api_impl = BMSTUScheduleAPI()
            case UniversityAlias.NSTU:
                self._api_impl = NSTUScheduleAPI()
            case UniversityAlias.STU:
                self._api_impl = STUScheduleAPI()

    async def group_exists(self, group_name: str) -> bool:
        return await self._api_impl.group_exists(group_name)

    async def fetch_schedule(self, group_name: str, day: date | None = None) -> list[Schedule]:
        return await self._api_impl.fetch_schedule(group_name, day)
