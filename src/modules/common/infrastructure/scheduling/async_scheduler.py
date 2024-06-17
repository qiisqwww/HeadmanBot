from collections.abc import Callable, Coroutine
from typing import Any

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from src.modules.common.infrastructure.bot_notifier import BotNotifierImpl

from .async_job import AsyncJob

__all__ = [
    "AsyncScheduler",
]


class AsyncScheduler:
    _scheduler: AsyncIOScheduler

    def __init__(self, bot: Bot, *jobs: AsyncJob) -> None:
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        for job in jobs:
            self._scheduler.add_job(
                self._job_wrapper(bot, job),
                trigger=job.trigger,
                **job.trigger_args,
            )

    @staticmethod
    def _job_wrapper(
        bot: Bot,
        job: AsyncJob,
    ) -> Callable[[], Coroutine[Any, Any, None]]:
        """APScheduler don't support async callable object and this wrapper solve this problem."""

        async def _job_wrapper_inner() -> None:
            job_name = job.__class__.__name__
            logger.info(f"Start job {job_name}.")

            try:
                await job()
            except Exception as e:
                notifier = BotNotifierImpl()
                await notifier.notify_about_job_exception(
                    e,
                    job_name,
                )
                logger.exception(e)

            logger.info(f"Stop job {job_name}.")

        return _job_wrapper_inner

    def start(self) -> None:
        self._scheduler.start()
