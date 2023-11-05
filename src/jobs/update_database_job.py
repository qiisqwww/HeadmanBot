import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config.config import DEBUG
from src.mirea_api import MireaScheduleApi
from src.services import UsersService

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

    def start(self):
        self._scheduler.start()

    @staticmethod
    async def _send():
        api = MireaScheduleApi()
        with UsersService() as con:
            groups = con.get_groups()
            for group in groups:
                try:
                    schedule = await api.get_schedule(group)
                except Exception as e:
                    logging.warning(f"EXCEPTION IN CLEARING USER DATA, {e}, {group}")
                    continue

                for user_id in con.get_user_of_group(group):
                    if not schedule:
                        con.change_attendance(user_id, "free")
                    else:
                        con.set_time(schedule[0].start_time, group)
                        con.change_attendance(user_id, f"start {len(schedule)}")
