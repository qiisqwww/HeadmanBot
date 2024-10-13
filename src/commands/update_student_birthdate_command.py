from datetime import date
from typing import final

from injector import inject

from src.common import UseCase
from src.modules.student_management.application.repositories import StudentRepository

__all__ = [
    "UpdateStudentBirthdateCommand",
]


@final
class UpdateStudentBirthdateCommand(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, student_id: int, birthdate: date | None) -> None:
        await self._repository.update_birthdate_by_id(student_id, birthdate)
