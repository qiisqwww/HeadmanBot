from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import (
    CacheStudentDataRepository,
)

__all__ = [
    "ClearCreateStudentDataCacheIfExistsCommand",
]


class ClearCreateStudentDataCacheIfExistsCommand(UseCase):
    _repository: CacheStudentDataRepository

    @inject
    def __init__(self, repository: CacheStudentDataRepository) -> None:
        self._repository = repository

    async def execute(self, telegram_id: int) -> None:
        if await self._repository.fetch(telegram_id):
            await self._repository.delete(telegram_id)
