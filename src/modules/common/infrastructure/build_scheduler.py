from typing import TYPE_CHECKING

from aiogram import Bot

from src.modules.attendance.infrastructure.jobs import MakeAttendanceRelevantJob
from src.modules.common.infrastructure.config import DEBUG
from src.modules.common.infrastructure.jobs import SendingJob, InformAboutUpdateJob
from src.modules.common.infrastructure.scheduling import AsyncScheduler
from src.modules.student_management.infrastructure.jobs import UnnoteAttendanceJob

from .container import project_container

__all__ = [
    "build_scheduler",
]

if TYPE_CHECKING:
    from src.modules.common.infrastructure.scheduling import AsyncJob


async def build_scheduler(bot: Bot) -> AsyncScheduler:
    attendance_jobs: list[AsyncJob] = []
    student_management_jobs: list[AsyncJob] = []
    common_jobs = [SendingJob(bot, project_container), InformAboutUpdateJob(bot, project_container)]

    if not DEBUG:
        attendance_jobs.append(MakeAttendanceRelevantJob(project_container))
        student_management_jobs.append(UnnoteAttendanceJob(project_container))

    return AsyncScheduler(*attendance_jobs, *student_management_jobs, *common_jobs)
