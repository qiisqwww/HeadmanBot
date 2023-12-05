from .attendance_service import AttendanceServiceImpl
from .group_service import GroupServiceImpl
from .lesson_service import LessonServiceImpl
from .registration_serice import RegistrationServiceImpl
from .student_service import StudentServiceImpl
from .university_service import UniversityServiceImpl

__all__ = [
    "UniversityServiceImpl",
    "GroupServiceImpl",
    "LessonServiceImpl",
    "AttendanceServiceImpl",
    "StudentServiceImpl",
    "RegistrationServiceImpl",
]
