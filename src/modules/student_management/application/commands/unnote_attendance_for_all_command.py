from typing import final

from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import StudentRepository

__all__ = [
    "UnnoteAttendanceForAllCommand",
]


@final
class UnnoteAttendanceForAllCommand(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self) -> None:
        await self._repository.update_attendance_noted_all(False)
