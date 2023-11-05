import json
from os import path

import requests
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.services import UsersService


class DownloadJob:
    _scheduler: AsyncIOScheduler

    def __init__(self, bot: Bot):
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
        self._scheduler.add_job(
            self._update_schedule, "cron", day_of_week="mon-sun", hour=0, minute=00, args=(bot.send_message,)
        )

    def start(self):
        self._scheduler.start()

    @staticmethod
    async def get_schedule():
        with UsersService() as con:
            for group in con.get_groups():
                req = requests.get(f"https://timetable.mirea.ru/api/groups/name/{group}").json()
                data = {group: req}

                with open("src/json/schedule.json", "w") as file:
                    json.dump(data, file)

    @staticmethod
    async def _update_schedule():
        """Just download schedule for each group if no json file.
        If it exists, necessary to download schedule for new groups"""
        if not path.exists("src/json/schedule.json"):
            await DownloadJob.get_schedule()
            return

        with UsersService() as con:
            downloaded_groups = list(json.load(open("src/json/schedule.json")).keys())  # list of groups from .json

            for group in con.get_groups():
                if group in downloaded_groups:
                    continue

                req = requests.get(f"https://timetable.mirea.ru/api/groups/name/{group}").json()
                data = {group: req}

                with open("src/json/schedule.json", "w") as file:
                    json.dump(data, file)
