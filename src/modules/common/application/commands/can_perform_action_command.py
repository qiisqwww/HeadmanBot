from injector import inject

from src.modules.common.application import Dependency
from src.modules.common.application.repositories.throttling_repository import ThrottlingRepository


class CanPerformActionCommand(Dependency):
    _repository: ThrottlingRepository

    @inject
    def __init__(self, repository: ThrottlingRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: str) -> int:
        throttling_rate = await self._repository.increase_user_throttling_rate(user_id)

        if throttling_rate == 1:
            await self._repository.set_execution_time(user_id)

        return throttling_rate < 10
