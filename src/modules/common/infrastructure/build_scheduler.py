from aiogram import Bot

from src.modules.attendance.infrastructure.jobs import MakeAttendanceRelevantJob
from src.modules.common.infrastructure.config import DEBUG
from src.modules.common.infrastructure.jobs import InformAboutUpdateJob, SendingJob
from src.modules.common.infrastructure.scheduling import AsyncScheduler
from src.modules.student_management.infrastructure.jobs import UnnoteAttendanceJob

from .container import project_container

__all__ = [
    "build_scheduler",
]


async def build_scheduler(bot: Bot) -> AsyncScheduler:
    attendance_jobs = [MakeAttendanceRelevantJob(project_container)]
    student_management_jobs = [UnnoteAttendanceJob(project_container)]
    common_jobs = [SendingJob(bot, project_container), InformAboutUpdateJob(bot, project_container)]

    if DEBUG:
        attendance_jobs = []
        student_management_jobs = []
        # common_jobs = []


    return AsyncScheduler(*attendance_jobs, *student_management_jobs, *common_jobs)
