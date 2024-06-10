from aiogram import Bot

from src.modules.attendance.infrastructure.jobs import MakeAttendanceRelevantJob
from src.modules.common.infrastructure.config import DEBUG
from src.modules.common.infrastructure.jobs import InformAboutUpdateJob, PollByRoleJob, SendingJob
from src.modules.common.infrastructure.scheduling import AsyncScheduler
from src.modules.student_management.infrastructure.jobs import UnnoteAttendanceJob

__all__ = [
    "build_scheduler",
]


async def build_scheduler(bot: Bot) -> AsyncScheduler:
    attendance_jobs = [MakeAttendanceRelevantJob(bot)]
    student_management_jobs = [UnnoteAttendanceJob(bot)]
    common_jobs = [
        SendingJob(bot),
        InformAboutUpdateJob(bot),
        PollByRoleJob(bot),
    ]

    if DEBUG:
        common_jobs = []
        attendance_jobs = []
        student_management_jobs = []

    return AsyncScheduler(bot, *attendance_jobs, *student_management_jobs, *common_jobs)
