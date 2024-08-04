from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import (
    CacheStudentEnterGroupDataRepository,
    StudentEnterGroupDTO,
)

__all__ = [
    "CacheStudentEnterGroupDataCommand",
]


class CacheStudentEnterGroupDataCommand(UseCase):
    _repository: CacheStudentEnterGroupDataRepository

    @inject
    def __init__(self, repository: CacheStudentEnterGroupDataRepository) -> None:
        self._repository = repository

    async def execute(self, data: StudentEnterGroupDTO) -> None:
        await self._repository.cache(data)
