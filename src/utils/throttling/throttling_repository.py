from typing import Final, final

from src.common.repositories import RedisRepository

__all__ = [
    "ThrottlingRepository",
]


@final
class ThrottlingRepository(RedisRepository):
    _THROTTLING_EXPIRE_TIME: Final[int] = 60  # One minute.

    async def increase_user_throttling_rate(self, user_id: str) -> int:
        return await self._con.incr(f"throttling_{user_id}")

    async def set_expire_time(self, user_id: str) -> None:
        await self._con.expire(f"throttling_{user_id}", self._THROTTLING_EXPIRE_TIME)
