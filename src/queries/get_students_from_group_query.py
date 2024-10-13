from typing import final

from injector import inject
from src.modules.student_management.application.repositories import StudentRepository

from src.common import UseCase
from src.dto.entities.student import Student

__all__ = [
    "GetStudentsFromGroupQuery",
]


@final
class GetStudentsFromGroupQuery(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, group_id: int) -> list[Student]:
        return await self._repository.filter_by_group_id(group_id)
