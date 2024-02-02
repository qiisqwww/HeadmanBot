from injector import inject
from loguru import logger

from src.modules.common.application import Dependency
from src.modules.common.application.repositories import ThrottlingRepository
from src.modules.common.infrastructure import THROTTLING_RATE_PER_MINUTE

__all__ = [
    "CanPerformActionCommand"
]


class CanPerformActionCommand(Dependency):
    _repository: ThrottlingRepository

    @inject
    def __init__(self, repository: ThrottlingRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: str) -> int:
        throttling_rate = await self._repository.increase_user_throttling_rate(user_id)
        logger.info(throttling_rate)

        if throttling_rate == 1:
            await self._repository.set_expire_time(user_id)
        return throttling_rate < THROTTLING_RATE_PER_MINUTE
