from aiogram import Bot
from src.modules.common.infrastructure.jobs import SendingJob
from src.modules.common.infrastructure.config import DEBUG
from src.modules.common.infrastructure.scheduling import AsyncScheduler
from src.modules.attendance.infrastructure.jobs import MakeAttendanceRelevantJob
from src.modules.student_management.infrastructure.jobs import UnmarkAllStudentsJob

from .container import project_container

__all__ = [
    "build_scheduler",
]


async def build_scheduler(bot: Bot) -> AsyncScheduler:
    attendance_jobs = []
    student_management_jobs = []
    common_jobs = [SendingJob(bot, project_container)]

    if not DEBUG:
        attendance_jobs.append(MakeAttendanceRelevantJob(project_container))
        student_management_jobs.append(UnmarkAllStudentsJob(project_container))

    return AsyncScheduler(*attendance_jobs, *student_management_jobs, *common_jobs)
