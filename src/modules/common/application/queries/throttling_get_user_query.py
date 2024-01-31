from injector import inject

from src.modules.common.application import Dependency
from src.modules.common.application.repositories.throttling_repository import ThrottlingRepository


class ThrottlingGetUserQuery(Dependency):
    _repository: ThrottlingRepository

    @inject
    def __init__(self, repository: ThrottlingRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: str) -> int | None:
        query: int | None = await self._repository.get_user_throttling(user_id)
        return query
