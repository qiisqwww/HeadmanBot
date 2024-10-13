from injector import inject

from src.common import UseCase
from src.modules.student_management.application.repositories import CacheStudentEnterGroupDataRepository

__all__ = [
    "ClearStudentEnterGroupDataCommand",
]


class ClearStudentEnterGroupDataCommand(UseCase):
    _repository: CacheStudentEnterGroupDataRepository

    @inject
    def __init__(self, repository: CacheStudentEnterGroupDataRepository) -> None:
        self._repository = repository

    async def execute(self, telegram_id: int) -> None:
        await self._repository.delete(telegram_id)
