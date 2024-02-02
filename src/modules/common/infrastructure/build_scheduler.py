from src.modules.common.infrastructure.scheduling import AsyncScheduler
from src.modules.attendance.infrastructure.jobs import MakeAttendanceRelevantJob
from src.modules.student_management.infrastructure.jobs import UnmarkAllStudentsJob

from .container import project_container

__all__ = [
    "build_scheduler",
]


async def build_scheduler() -> AsyncScheduler:
    attendance_jobs = [MakeAttendanceRelevantJob(project_container),]
    student_management_jobs = [UnmarkAllStudentsJob(project_container)]

    return AsyncScheduler(*attendance_jobs, *student_management_jobs)
