from datetime import date
from typing import NoReturn, final

from src.modules.common.domain import UniversityAlias
from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.domain import Schedule

from .impls import BmstuScheduleApi, MireaScheduleApi

__all__ = [
    "ScheduleApiImpl",
]


@final
class ScheduleApiImpl(ScheduleAPI):
    _api_impl: ScheduleAPI

    def __init__(self, university: UniversityAlias) -> None:
        match university:
            case UniversityAlias.MIREA:
                self._api_impl = MireaScheduleApi()
            case UniversityAlias.BMSTU:
                self._api_impl = BmstuScheduleApi()

    async def group_exists(self, group_name: str) -> bool | NoReturn:
        return await self._api_impl.group_exists(group_name)

    async def fetch_schedule(self, group_name: str, day: date | None = None) -> list[Schedule] | NoReturn:
        return await self._api_impl.fetch_schedule(group_name, day)
