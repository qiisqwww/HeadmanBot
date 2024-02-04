from typing import final

from src.modules.common.infrastructure import THROTTLING_EXPIRE_TIME
from src.modules.common.infrastructure.repositories import RedisRepositoryImpl
from src.modules.utils.throttling.application.repositories import ThrottlingRepository

__all__ = [
    "ThrottlingRepositoryImpl",
]


@final
class ThrottlingRepositoryImpl(ThrottlingRepository, RedisRepositoryImpl):
    async def increase_user_throttling_rate(self, user_id: str) -> int:
        return await self._con.incr(f"throttling_{user_id}")

    async def set_expire_time(self, user_id: str) -> None:
        await self._con.expire(f"throttling_{user_id}", THROTTLING_EXPIRE_TIME)
