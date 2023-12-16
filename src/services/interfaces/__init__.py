from .attendance_service_interface import AttendanceService
from .group_service_interface import GroupService
from .lesson_service_interface import LessonService
from .registration_service_interface import RegistrationService
from .service import Service
from .student_service_interface import StudentService
from .university_service_interface import UniversityService
from .redis_service import RedisService

__all__ = [
    "Service",
    "AttendanceService",
    "UniversityService",
    "LessonService",
    "GroupService",
    "StudentService",
    "RegistrationService",
    "RedisService"
]
