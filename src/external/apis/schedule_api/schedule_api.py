import httpx
from loguru import logger

from src.enums import UniversityAlias

from .dto import Schedule
from .enums import Weekday
from .exceptions import FailedToCheckGroupExistence, FailedToFetchScheduleException
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
        try:
            return await self._api_impl.group_exists(group_name)
        except httpx.ConnectTimeout as e:
            logger.error(e)
            raise FailedToCheckGroupExistence from e

    async def fetch_schedule(self, group_name: str, weekday: Weekday | None = None) -> list[Schedule]:
        try:
            return await self._api_impl.fetch_schedule(group_name, weekday)
        except httpx.ConnectTimeout as e:
            logger.error(e)
            raise FailedToFetchScheduleException from e
