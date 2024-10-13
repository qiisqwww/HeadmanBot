from typing import final

from injector import inject

from src.common import UseCase
from src.modules.student_management.application.repositories import StudentRepository

__all__ = [
    "UpdateStudentFirstNameCommand",
]


@final
class UpdateStudentFirstNameCommand(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, student_id: int, new_first_name: str) -> None:
        await self._repository.update_first_name_by_id(student_id, new_first_name)
