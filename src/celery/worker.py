import asyncio

from aiogram import Bot
from celery import Celery
from celery.schedules import crontab

from src.modules.attendance.application.commands import MakeAttendanceRelevantCommand
from src.modules.common.application import NoArgsUseCase
from src.modules.common.infrastructure.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from src.modules.common.infrastructure.config.config import BOT_TOKEN, DEBUG
from src.modules.common.infrastructure.container import Container

worker = Celery(__name__)
worker.conf.broker_url = CELERY_BROKER_URL
worker.conf.result_backend = CELERY_RESULT_BACKEND
worker.conf.timezone = "Europe/Moscow"
worker.autodiscover_tasks()


def execute_action(action: type[NoArgsUseCase]) -> None:
    async def _async_wrapper() -> None:
        await Container.init(Bot(BOT_TOKEN))
        async with Container() as container:
            command = container.get_dependency(action)
            await command.execute()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_async_wrapper())


@worker.task(name="Make attendance relevant")
def make_attendance_relevant() -> None:
    execute_action(MakeAttendanceRelevantCommand)


worker.conf.beat_schedule = {
    "make_attendance_relevant": {
        "task": "Make attendance relevant",
        "schedule": crontab(hour="19", minute="55"),
    },
}


def start_tasks_for_debug() -> None:
    make_attendance_relevant.delay()
