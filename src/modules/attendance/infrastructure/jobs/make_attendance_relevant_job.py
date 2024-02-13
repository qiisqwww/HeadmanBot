from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import final

from aiogram import Bot
from injector import Injector

from src.modules.attendance.application.commands import MakeAttendanceRelevantCommand
from src.modules.common.infrastructure.config import DEBUG
from src.modules.common.infrastructure.scheduling import AsyncJob

__all__ = [
    "MakeAttendanceRelevantJob",
]


@final
class MakeAttendanceRelevantJob(AsyncJob):
    _build_container: Callable[[], AbstractAsyncContextManager[Injector]]
    _bot: Bot

    def __init__(
        self,
        bot: Bot,
        build_container: Callable[[], AbstractAsyncContextManager[Injector]],
    ) -> None:
        self._build_container = build_container
        self._bot = bot

        if not DEBUG:
            self._trigger = "cron"
            self._trigger_args = {
                "hour": 1,
                "minute": 0,
                "day_of_week": "mon-sun",
            }

    async def __call__(self) -> None:
        async with self._build_container() as container:
            command = container.get(MakeAttendanceRelevantCommand)
            await command.execute(self._bot)
