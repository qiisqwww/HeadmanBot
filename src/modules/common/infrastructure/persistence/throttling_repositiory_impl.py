from src.modules.common.infrastructure.persistence import RedisRepositoryImpl
from src.modules.common.application.repositories.throttling_repository import ThrottlingRepository


class ThrottlingRepositoryImpl(ThrottlingRepository, RedisRepositoryImpl):
    async def set_user_throttling(self, user_id: str) -> None:
        await self._con.set(f"throttling&{user_id}", 0, ex=15)

    async def increase_user_throttling(self, user_id: str) -> None:
        await self._con.incr(f"throttling&{user_id}")

    async def get_user_throttling(self, user_id: str) -> int | None:
        return await self._con.get(f"throttling&{user_id}")
