from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from src.config import DEBUG
from src.database import get_pool
from src.services import AttendanceService, LessonService

__all__ = [
    "UpdateDatabaseJob",
]


class UpdateDatabaseJob:
    """Update lessons and attendances for current day."""

    _scheduler: AsyncIOScheduler

    def __init__(self):
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if DEBUG:
            self._scheduler.add_job(self._update)
        else:
            self._scheduler.add_job(self._update, "cron", day_of_week="mon-sun", hour=2, minute=00)

    def start(self) -> None:
        self._scheduler.start()

    @staticmethod
    @logger.catch
    async def _update() -> None:
        pool = await get_pool()

        async with pool.acquire() as con:
            lesson_service = LessonService(con)
            await lesson_service.recreate_lessons()

            attendance_service = AttendanceService(con)
            await attendance_service.recreate_attendances()
