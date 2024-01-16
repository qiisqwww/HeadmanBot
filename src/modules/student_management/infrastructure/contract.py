from dataclasses import asdict
from typing import Any, final

from injector import inject

from src.modules.student_management.application.repositories import (
    StudentInfoRepository,
    StudentRepository,
)
from src.modules.student_management.contract import StudentManagementContract

__all__ = [
    "StudentManagementContractImpl",
]


@final
class StudentManagementContractImpl(StudentManagementContract):
    _student_info_repository: StudentInfoRepository
    _student_repostory: StudentRepository

    @inject
    def __init__(self, student_info_repository: StudentInfoRepository, student_repository: StudentRepository) -> None:
        self._student_info_repository = student_info_repository
        self._student_repostory = student_repository

    async def get_students_info(self, group_id: int) -> list[dict[str, Any]]:
        return [
            asdict(student_info) for student_info in (await self._student_info_repository.filter_by_group_id(group_id))
        ]

    async def update_checked_in_status(self, student_id: int, previous_is_checked_in: bool) -> None:
        if not previous_is_checked_in:
            await self._student_repostory.update_is_checked_in(student_id, True)
