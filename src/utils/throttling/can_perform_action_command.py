from typing import final

from redis.asyncio import Redis

from src.common.config import THROTTLING_RATE_PER_MINUTE
from src.common.use_case import UseCase
from .throttling_repository import ThrottlingRepository

__all__ = [
    "CanPerformActionCommand",
]


@final
class CanPerformActionCommand(UseCase):
    _repository: ThrottlingRepository

    def __init__(self, redis_con: Redis) -> None:
        self._repository = ThrottlingRepository(redis_con)

    async def execute(self, telegram_id: int) -> int:
        telegram_id = str(telegram_id)
        throttling_rate = await self._repository.increase_user_throttling_rate(telegram_id)

        if throttling_rate == 1:
            await self._repository.set_expire_time(telegram_id)
        return throttling_rate <= THROTTLING_RATE_PER_MINUTE
