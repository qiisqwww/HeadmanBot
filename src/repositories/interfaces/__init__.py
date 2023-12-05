from .attendance_repository_interface import AttendanceRepository
from .group_repository_interface import GroupRepository
from .lesson_repository_interface import LessonRepository
from .postgres_repository_interface import PostgresRepository
from .student_repository_interface import StudentRepository
from .university_repository_interface import UniversityRepository

__all__ = [
    "GroupRepository",
    "PostgresRepository",
    "UniversityRepository",
    "LessonRepository",
    "AttendanceRepository",
    "StudentRepository",
]
