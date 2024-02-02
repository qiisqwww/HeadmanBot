from src.modules.common.infrastructure.persistence import RedisRepositoryImpl
from src.modules.common.application.repositories.throttling_repository import ThrottlingRepository


class ThrottlingRepositoryImpl(ThrottlingRepository, RedisRepositoryImpl):

    async def increase_user_throttling_rate(self, user_id: str) -> int:
        await self._con.incr(f"throttling&{user_id}")
        return await self._con.get(f"throttling{user_id}")

    async def set_execution_time(self, user_id: str) -> None:
        await self._con.expire(user_id)
