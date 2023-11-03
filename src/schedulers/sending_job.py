import logging
from typing import Callable

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import DEBUG
from src.messages import POLL_MESSAGE
from src.buttons import load_attendance_kb
from src.work_api import API
from src.services import UsersService


class SendingJob:
    _scheduler: AsyncIOScheduler
    _api: API

    def __init__(self, bot: Bot):
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if DEBUG:
            self._scheduler.add_job(self._send,
                                    "interval",
                                    seconds=10,
                                    args=(bot.send_message, ))
        else:
            self._scheduler.add_job(self._send,
                                    "cron",
                                    day_of_week="mon-sun",
                                    hour=7,
                                    minute=00,
                                    args=(bot.send_message, ))

    def start(self):
        self._scheduler.start()

    @staticmethod
    async def _send(poll_user: Callable):
        api = API()
        with UsersService() as con:
            groups = con.get_groups()
            for group in groups:
                try:
                    api.regenerate(group[0])
                    day = api.get_today()

                except Exception as e:
                    logging.warning(f"EXCEPTION IN GENERATING LESSONS (API), {e}, {group[0]}")
                    continue

                if len(day) == 0:
                    continue

                for user_id in con.get_user_of_group(group[0]):
                    try:
                        await poll_user(user_id, POLL_MESSAGE, reply_markup=load_attendance_kb(day))
                    except Exception as e:
                        logging.warning(f"EXCEPTION IN POLL, {e}")
