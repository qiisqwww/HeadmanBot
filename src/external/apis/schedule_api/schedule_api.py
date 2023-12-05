from src.enums import UniversityAlias

from .dto import Schedule
from .enums import Weekday
from .impls import BmstuScheduleApi, MireaScheduleApi
from .schedule_api_interface import IScheduleAPI

__all__ = [
    "ScheduleApi",
]


class ScheduleApi:
    _api_impl: IScheduleAPI

    def __init__(self, university: UniversityAlias) -> None:
        match university:
            case UniversityAlias.MIREA:
                self._api_impl = MireaScheduleApi()
            case UniversityAlias.BMSTU:
                self._api_impl = BmstuScheduleApi()

    async def group_exists(self, group_name: str) -> bool:
        return await self._api_impl.group_exists(group_name)

    async def fetch_schedule(self, group_name: str, weekday: Weekday | None = None) -> list[Schedule]:
        return await self._api_impl.fetch_schedule(group_name, weekday)
