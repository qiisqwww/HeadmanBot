from typing import final

from injector import inject

from src.common import UseCase
from src.modules.student_management.application.repositories import StudentRepository

__all__ = [
    "UpdateStudentLastNameCommand",
]


@final
class UpdateStudentLastNameCommand(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, student_id: int, new_last_name: str) -> None:
        await self._repository.update_last_name_by_id(student_id, new_last_name)
