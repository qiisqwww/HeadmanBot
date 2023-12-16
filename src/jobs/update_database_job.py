from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from asyncpg.pool import Pool

from src.config import DEBUG
from src.services.impls import (
    StudentServiceImpl,
    GroupServiceImpl,
    LessonServiceImpl,
    UniversityServiceImpl,
    AttendanceServiceImpl
)
from src.repositories.impls import (
    StudentRepositoryImpl,
    GroupRepositoryImpl,
    LessonRepositoryImpl,
    UniversityRepositoryImpl,
    AttendanceRepositoryImpl
)

__all__ = [
    "UpdateDatabaseJob",
]


class UpdateDatabaseJob:
    """Update lessons and attendances for current day."""

    _scheduler: AsyncIOScheduler

    def __init__(
            self,
            pool: Pool
    ):
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if DEBUG:
            self._scheduler.add_job(
                self._update,
                trigger="interval",
                seconds=20,
                args=(pool,)
            )
        else:
            self._scheduler.add_job(
                self._update,
                trigger="cron",
                day_of_week="mon-sun",
                hour=2,
                minute=00,
                args=(pool,)
            )

    async def start(self) -> None:
        self._scheduler.start()

    @staticmethod
    @logger.catch
    async def _update(pool: Pool) -> None:
        async with pool.acquire() as con:
            group_service = GroupServiceImpl(GroupRepositoryImpl(con))
            university_service = UniversityServiceImpl(UniversityRepositoryImpl(con))
            student_service = StudentServiceImpl(
                StudentRepositoryImpl(con),
                group_service,
                university_service
            )
            lesson_service = LessonServiceImpl(
                LessonRepositoryImpl(con),
                group_service,
                university_service
            )

            attendance_service = AttendanceServiceImpl(
                AttendanceRepositoryImpl(con),
                lesson_service,
                student_service
            )

            await lesson_service.recreate_lessons()
            await attendance_service.recreate_attendances()
