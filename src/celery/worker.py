import asyncio

from aiogram import Bot
from celery import Celery
from celery.schedules import crontab

from src.modules.attendance.application.commands import MakeAttendanceRelevantCommand
from src.modules.common.application import NoArgsUseCase
from src.modules.common.application.command import AskAttendanceCommand
from src.modules.common.infrastructure.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from src.modules.common.infrastructure.config.config import BOT_TOKEN
from src.modules.common.infrastructure.container import Container
from src.modules.student_management.application.commands import UnnoteAttendanceForAllCommand

worker = Celery(__name__)
worker.conf.broker_url = CELERY_BROKER_URL
worker.conf.result_backend = CELERY_RESULT_BACKEND
worker.conf.timezone = "Europe/Moscow"
worker.autodiscover_tasks()


def execute_command(action: type[NoArgsUseCase], bot_token: str = BOT_TOKEN) -> None:
    async def _async_wrapper() -> None:
        await Container.init(Bot(bot_token))
        async with Container() as container:
            command = container.get_dependency(action)
            await command.execute()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_async_wrapper())


@worker.task(name="Make attendance relevant")
def make_attendance_relevant_task() -> None:
    execute_command(MakeAttendanceRelevantCommand)


@worker.task(name="Ask attendance")
def ask_attendance_task() -> None:
    execute_command(AskAttendanceCommand)

@worker.task(name="Unnote attendance")
def unnote_students_attendance() -> None:
    execute_command(UnnoteAttendanceForAllCommand)


worker.conf.beat_schedule = {
    "make_attendance_relevant": {
        "task": "Make attendance relevant",
        "schedule": crontab(hour="1", minute="0", day_of_week="mon-sun"),
    },

    "unnote_students_attendance": {
        "task": "Unnote attendance",
        "schedule": crontab(hour="1", minute="0", day_of_week="mon-sun"),
    },

    "ask_attendance": {
        "task": "Ask attendance",
        "schedule": crontab(hour="7", minute="0", day_of_week="mon-sat"),
    },
}


def start_tasks_for_debug() -> None:
    make_attendance_relevant_task.delay()
    ask_attendance_task.delay()
