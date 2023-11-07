from .attendance_service import AttendanceService
from .group_service import GroupService
from .lesson_service import LessonService
from .schedule_service import ScheduleService
from .student_service import StudentService
from .university_service import UniversityService

__all__ = [
    "GroupService",
    "StudentService",
    "UniversityService",
    "AttendanceService",
    "LessonService",
    "ScheduleService",
]
