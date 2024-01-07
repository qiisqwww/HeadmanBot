from src.modules.student_management.application.repositories import CreateStudentDTO

from ..repositories import CacheStudentDataRepository

__all__ = [
    "CacheCreateStudentDataCommand",
]


class CacheCreateStudentDataCommand:
    _repository: CacheStudentDataRepository

    def __init__(self, repository: CacheStudentDataRepository) -> None:
        self._repository = repository

    async def execute(self, data: CreateStudentDTO) -> None:
        await self._repository.cache(data)
