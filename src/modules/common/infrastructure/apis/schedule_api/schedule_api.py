import httpx
from loguru import logger

from src.modules.common.application.schedule_api import Schedule, ScheduleAPI, Weekday
from src.modules.common.domain import UniversityAlias

from .exceptions import FailedToCheckGroupExistence, FailedToFetchScheduleException
from .impls import BmstuScheduleApi, MireaScheduleApi

__all__ = [
    "ScheduleApiImpl",
]


class ScheduleApiImpl(ScheduleAPI):
    _api_impl: ScheduleAPI

    def __init__(self, university: UniversityAlias) -> None:
        match university:
            case UniversityAlias.MIREA:
                self._api_impl = MireaScheduleApi()
            case UniversityAlias.BMSTU:
                self._api_impl = BmstuScheduleApi()

    async def group_exists(self, group_name: str) -> bool:
        try:
            return await self._api_impl.group_exists(group_name)
        except httpx.ConnectTimeout as e:
            logger.exception(e)
            raise FailedToCheckGroupExistence from e

    async def fetch_schedule(self, group_name: str, weekday: Weekday | None = None) -> list[Schedule]:
        try:
            return await self._api_impl.fetch_schedule(group_name, weekday)
        except httpx.ConnectTimeout as e:
            logger.exception(e)
            raise FailedToFetchScheduleException from e
