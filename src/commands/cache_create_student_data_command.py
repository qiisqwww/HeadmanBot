from injector import inject

from src.common import UseCase
from src.modules.student_management.application.repositories import CacheCreateStudentDataRepository, CreateStudentDTO

__all__ = [
    "CacheCreateStudentDataCommand",
]


class CacheCreateStudentDataCommand(UseCase):
    _repository: CacheCreateStudentDataRepository

    @inject
    def __init__(self, repository: CacheCreateStudentDataRepository) -> None:
        self._repository = repository

    async def execute(self, data: CreateStudentDTO) -> None:
        await self._repository.cache(data)
