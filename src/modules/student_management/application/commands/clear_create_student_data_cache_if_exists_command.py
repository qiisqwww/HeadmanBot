from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import CacheCreateStudentDataRepository

__all__ = [
    "ClearCreateStudentDataCacheIfExistsCommand",
]


class ClearCreateStudentDataCacheIfExistsCommand(UseCase):
    _repository: CacheCreateStudentDataRepository

    @inject
    def __init__(self, repository: CacheCreateStudentDataRepository) -> None:
        self._repository = repository

    async def execute(self, telegram_id: int) -> None:
        if await self._repository.fetch(telegram_id):
            await self._repository.delete(telegram_id)
