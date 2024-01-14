from dataclasses import asdict
from typing import Any, final

from injector import inject

from src.modules.student_management.application.repositories import (
    StudentInfoRepository,
)
from src.modules.student_management.contract import StudentManagementContract

__all__ = [
    "StudentManagementContractImpl",
]


@final
class StudentManagementContractImpl(StudentManagementContract):
    _repository: StudentInfoRepository

    @inject
    def __init__(self, repository: StudentInfoRepository) -> None:
        self._repository = repository

    async def get_students_info(self, group_id: int) -> list[dict[str, Any]]:
        return [asdict(student_info) for student_info in (await self._repository.filter_by_group_id(group_id))]
