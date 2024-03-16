from typing import final

from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import StudentRepository
from src.modules.student_management.domain.enums.role import Role

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
        self, group_id: int, last_name: str, first_name: str,
    ) -> int | None:
        student = await self._repository.find_by_fullname_and_group_id(
            last_name,
            first_name,
            group_id,
        )

        if student is None:
            print("Not registered")
            return None

        if student.role != Role.VICE_HEADMAN:
            print("Only vice headman can be popushen`")
            return None

        await self._repository.set_role_by_id(student.id, Role.STUDENT)
        return student.id
