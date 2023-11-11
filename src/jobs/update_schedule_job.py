from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import DEBUG
from src.database import get_pool
from src.services import ScheduleService

__all__ = [
    "UpdateScheduleJob",
]


class UpdateScheduleJob:
    """Download schedule for current week"""

    _scheduler: AsyncIOScheduler

    def __init__(self):
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if DEBUG:
            self._scheduler.add_job(self._send)
        else:
            self._scheduler.add_job(self._send, "cron", day_of_week="mon", hour=1, minute=00)

    def start(self):
        self._scheduler.start()

    @staticmethod
    async def _send() -> None:
        pool = await get_pool()

        async with pool.acquire() as conn:
            schedule_service = ScheduleService(conn)
            await schedule_service.recreate_shedule()
