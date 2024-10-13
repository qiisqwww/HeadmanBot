import asyncio

from celery import Celery
from celery.app.log import Logging
from celery.schedules import crontab

from src.commands import MakeAttendanceRelevantCommand, UnnoteAttendanceForAllCommand, AskAttendanceCommand
from src.common.bot_notifier import BotNotifier
from src.common.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from src.common.database import DbContext, create_db_pool
from src.common.facade import Facade
from src.common.use_case import NoArgsUseCase

worker = Celery(__name__)
worker.conf.broker_url = CELERY_BROKER_URL
worker.conf.result_backend = CELERY_RESULT_BACKEND
worker.conf.timezone = "Europe/Moscow"
worker.autodiscover_tasks()

logging = Logging(worker)
logging.setup(loglevel="info", logfile="logs/logging-info.log")
logging.setup(loglevel="error", logfile="logs/logging-error.log")


# configure_logger()

def execute_command(action: type[NoArgsUseCase]) -> None:
    async def _async_wrapper() -> None:
        try:
            async with DbContext() as con:
                command = action(con=con)
                await command.execute()
        except Exception as e:
            await BotNotifier().notify_about_job_exception(e, action.__name__)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_async_wrapper())


def execute_facade(action: type[Facade]) -> None:
    async def _async_wrapper() -> None:
        try:
            with create_db_pool() as pool:
                command = action(pool=pool)
                await command.execute()
        except Exception as e:
            await BotNotifier().notify_about_job_exception(e, action.__name__)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_async_wrapper())


@worker.task(name="Make attendance relevant")
def make_attendance_relevant_task() -> None:
    execute_command(MakeAttendanceRelevantCommand)


@worker.task(name="Ask attendance")
def ask_attendance_task() -> None:
    execute_facade(AskAttendanceCommand)


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
