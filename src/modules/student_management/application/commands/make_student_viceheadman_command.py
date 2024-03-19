from typing import final

from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import StudentRepository
from src.modules.student_management.domain.enums.role import Role

from .exceptions import CannotGrantRoleToNonStudentError, StudentNotFoundError

__all__ = [
    "MakeStudentViceHeadmanCommand",
]


@final
class MakeStudentViceHeadmanCommand(UseCase):
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

        if student.role != Role.STUDENT:
            raise CannotGrantRoleToNonStudentError

        await self._repository.set_role_by_id(student.id, Role.VICE_HEADMAN)
