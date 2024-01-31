from injector import inject

from src.modules.common.application import Dependency
from src.modules.common.application.repositories.throttling_repository import ThrottlingRepository


class ThrottlingSetUserCommand(Dependency):
    _repository: ThrottlingRepository

    @inject
    def __init__(self, repository: ThrottlingRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: str) -> None:
        await self._repository.set_user_throttling(user_id)
