from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import CacheStudentDataRepository

__all__ = [
    "ClearCreateStudentDataCacheCommand",
]


class ClearCreateStudentDataCacheCommand(UseCase):
    _repository: CacheStudentDataRepository

    @inject
    def __init__(self, repository: CacheStudentDataRepository) -> None:
        self._repository = repository

    async def execute(self, telegram_id: int) -> None:
        await self._repository.pop(telegram_id)
