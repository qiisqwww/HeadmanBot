import asyncio

from aiogram.client.bot import Bot
from celery import Celery
from celery.schedules import crontab

from src.modules.attendance.application.commands import MakeAttendanceRelevantCommand
from src.modules.common.infrastructure.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from src.modules.common.infrastructure.config.config import BOT_TOKEN, DEBUG
from src.modules.common.infrastructure.container import Container

worker = Celery(__name__)
worker.conf.broker_url = CELERY_BROKER_URL
worker.conf.result_backend = CELERY_RESULT_BACKEND
worker.conf.timezone = "Europe/Moscow"


@worker.task(name="Make attendance relevant")
def make_attendance_relevant() -> None:
    async def _wrapper() -> None:
        await Container.init(Bot(BOT_TOKEN))
        async with Container() as container:
            command = container.get_dependency(MakeAttendanceRelevantCommand)
            await command.execute()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_wrapper())
