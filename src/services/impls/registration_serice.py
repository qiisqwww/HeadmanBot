from src.dto.models import StudentRaw
from src.repositories import StudentRepository
from src.services.interfaces import (
    AttendanceService,
    GroupService,
    RegistrationService,
    UniversityService,
)

__all__ = [
    "RegistrationServiceImpl",
]


class RegistrationServiceImpl(RegistrationService):
    _student_repository: StudentRepository
    _attendance_service: AttendanceService
    _group_service: GroupService
    _university_service: UniversityService

    def __init__(
        self,
        student_repository: StudentRepository,
        attendance_service: AttendanceService,
        group_service: GroupService,
        university_service: UniversityService,
    ) -> None:
        self._student_repository = student_repository
        self._attendance_service = attendance_service
        self._group_service = group_service
        self._university_service = university_service

    async def register_student(self, student_raw: StudentRaw) -> None:
        university = await self._university_service.get_by_alias(student_raw.university_alias)
        new_group = await self._group_service.create_or_return(
            student_raw.group_name,
            university.id,
        )

        new_student = await self._student_repository.create_and_return(student_raw, new_group.id)
        await self._attendance_service.create_for_student(new_student)
