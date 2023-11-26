from .attendance_service import AttendanceService
from .auth_contract_service import AuthContractService
from .group_service import GroupService
from .lesson_service import LessonService
from .student_service import StudentService
from .university_service import UniversityService

__all__ = [
    "AttendanceService",
    "GroupService",
    "LessonService",
    "StudentService",
    "UniversityService",
    "AuthContractService",
]
