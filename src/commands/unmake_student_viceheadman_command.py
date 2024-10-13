from typing import final

from injector import inject
from src.modules.student_management.application.commands.exceptions import (
    CannotDowngradeNonViceHeadmanError,
    StudentNotFoundError,
)
from src.modules.student_management.application.repositories import StudentRepository

from src.common import UseCase
from src.dto.enums.role import Role

__all__ = [
    "UnmakeStudentViceHeadmanCommand",
]


@final
class UnmakeStudentViceHeadmanCommand(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(
            self,
            repository: StudentRepository,
    ) -> None:
        self._repository = repository

    async def execute(
            self,
            student_id: int,
    ) -> None:
        student = await self._repository.find_by_id(
            student_id,
        )

        if student is None:
            raise StudentNotFoundError

        if student.role != Role.VICE_HEADMAN:
            raise CannotDowngradeNonViceHeadmanError

        await self._repository.set_role_by_id(student.id, Role.STUDENT)
