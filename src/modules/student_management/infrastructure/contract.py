from dataclasses import asdict
from typing import Any, final

from injector import inject

from src.modules.student_management.application.repositories import (
    StudentInfoRepository,
    StudentRepository,
)
from src.modules.student_management.contract import StudentManagementContract
from src.modules.student_management.domain.enums import Role

__all__ = [
    "StudentManagementContractImpl",
]


@final
class StudentManagementContractImpl(StudentManagementContract):
    _student_info_repository: StudentInfoRepository
    _student_repository: StudentRepository

    @inject
    def __init__(self, student_info_repository: StudentInfoRepository, student_repository: StudentRepository) -> None:
        self._student_info_repository = student_info_repository
        self._student_repository = student_repository

    async def get_students_info(self, group_id: int) -> list[dict[str, Any]]:
        return [
            asdict(student_info) for student_info in (await self._student_info_repository.filter_by_group_id(group_id))
        ]

    async def get_headman_by_group_id(self, group_id: int) -> dict:
        return asdict(await self._student_repository.find_by_group_id_and_role(group_id, role=Role.HEADMAN))

    async def note_student_attendance(self, student_id: int) -> None:
        await self._student_repository.update_attendance_noted_by_id(student_id, True)
