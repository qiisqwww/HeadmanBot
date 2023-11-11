from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import DEBUG
from src.database import get_pool
from src.services import AttendanceService

__all__ = [
    "UpdateDatabaseJob",
]


class UpdateDatabaseJob:
    """Set correct start time of first lesson for today schedule."""

    _scheduler: AsyncIOScheduler

    def __init__(self):
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if DEBUG:
            self._scheduler.add_job(self._send)
        else:
            self._scheduler.add_job(self._send, "cron", day_of_week="mon-sun", hour=2, minute=00)

    def start(self) -> None:
        self._scheduler.start()

    @staticmethod
    async def _send() -> None:
        pool = await get_pool()
        async with pool.acquire() as conn:
            attendance_service = AttendanceService(conn)

            await attendance_service.recreate_all_attendance()
