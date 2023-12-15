from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from src.config import DEBUG
from src.services import AttendanceService, LessonService

__all__ = [
    "UpdateDatabaseJob",
]


class UpdateDatabaseJob:
    """Update lessons and attendances for current day."""

    _scheduler: AsyncIOScheduler

    def __init__(
            self,
            lesson_service: LessonService,
            attendance_service: AttendanceService
    ):
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if DEBUG:
            self._scheduler.add_job(self._update)
        else:
            self._scheduler.add_job(
                self._update,
                trigger="cron",
                day_of_week="mon-sun",
                hour=2,
                minute=00,
                args=(
                    lesson_service,
                    attendance_service
                )
            )

    def start(self) -> None:
        self._scheduler.start()

    @staticmethod
    @logger.catch
    async def _update(
            lesson_service: LessonService,
            attendance_service: AttendanceService
    ) -> None:
        await lesson_service.recreate_lessons()
        await attendance_service.recreate_attendances()
