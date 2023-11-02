from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import DEBUG
from poll import job

__all__ = [
    "SendingScheduler",
]


class SendingScheduler(AsyncIOScheduler):
    def __init__(self, bot: Bot):
        super().__init__(timezone="Europe/Moscow")

        if DEBUG:
            self.add_job(job, "interval", seconds=10, args=(bot.send_message,))
        else:
            self.add_job(job, "cron", day_of_week="mon-sun", hour=7, minute=00, args=(bot.send_message,))
