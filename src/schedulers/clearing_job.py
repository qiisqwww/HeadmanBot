import logging
from typing import Callable

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import DEBUG
from src.messages import POLL_MESSAGE
from src.buttons import load_attendance_kb
from src.work_api import API
from src.services import UsersService


class ClearingJob:
    _scheduler: AsyncIOScheduler

    def __init__(self):
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if DEBUG:
            self._scheduler.add_job(self._send,
                                    "interval",
                                    seconds=60)
        else:
            self._scheduler.add_job(self._send,
                                    "cron",
                                    day_of_week="mon-sun",
                                    hour=2,
                                    minute=00)

    def start(self):
        self._scheduler.start()

    @staticmethod
    async def _send():
        api = API()
        with UsersService() as con:
            groups = con.get_groups()
            for group in groups:
                try:
                    api.regenerate(group)
                    day = api.get_today()
                except Exception as e:
                    logging.warning(f"EXCEPTION IN CLEARING USER DATA, {e}, {group}")
                    continue

                for user_id in con.get_user_of_group(group):
                    if len(day) == 0:
                        print(user_id)
                        con.change_attendance(user_id, "free")
                    else:
                        con.set_time(day[0][1], group)
                        con.change_attendance(user_id, f'start {len(day)}')

                    con.set_not_polled(user_id)
