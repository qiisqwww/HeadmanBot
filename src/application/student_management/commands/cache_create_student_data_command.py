from src.application.student_management.repositories.create_student_dto import (
    CreateStudentDTO,
)

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
