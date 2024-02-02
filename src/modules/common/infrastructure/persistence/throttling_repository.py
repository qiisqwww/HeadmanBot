from src.modules.common.infrastructure.persistence import RedisRepositoryImpl
from src.modules.common.application.repositories import ThrottlingRepository
from src.modules.common.infrastructure import THROTTLING_EXPIRE_TIME

__all__ = [
    "ThrottlingRepositoryImpl"
]


class ThrottlingRepositoryImpl(ThrottlingRepository, RedisRepositoryImpl):

    async def increase_user_throttling_rate(self, user_id: str) -> int:
        await self._con.incr(f"throttling_{user_id}")
        return int(await self._con.get(f"throttling_{user_id}"))

    async def set_expire_time(self, user_id: str) -> None:
        await self._con.expire(f"throttling_{user_id}", THROTTLING_EXPIRE_TIME)
