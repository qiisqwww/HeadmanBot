from abc import abstractmethod

from src.dto import StudentRaw
from src.repositories import StudentRepository

from .attendance_service_interface import AttendanceService
from .group_service_interface import GroupService
from .service import Service
from .university_service_interface import UniversityService

__all__ = [
    "RegistrationService",
]


class RegistrationService(Service):
    @abstractmethod
    def __init__(
        self,
        student_repository: StudentRepository,
        attendance_service: AttendanceService,
        group_service: GroupService,
        university_service: UniversityService,
    ) -> None:
        ...

    @abstractmethod
    async def register_student(self, student_raw: StudentRaw) -> None:
        ...
