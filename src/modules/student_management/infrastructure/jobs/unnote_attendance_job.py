from typing import final

from aiogram import Bot

from src.modules.common.infrastructure.config import DEBUG
from src.modules.common.infrastructure.container import Container
from src.modules.common.infrastructure.scheduling import AsyncJob
from src.modules.student_management.application.commands import (
    UnnoteAttendanceForAllCommand,
)

__all__ = [
    "UnnoteAttendanceJob",
]


@final
class UnnoteAttendanceJob(AsyncJob):
    _bot: Bot

    def __init__(self, bot: Bot) -> None:
        self._bot = bot

        if not DEBUG:
            self._trigger = "cron"
            self._trigger_args = {
                "hour": 1,
                "minute": 00,
                "day_of_week": "mon-sun",
            }

    async def __call__(self) -> None:
        async with Container() as container:
            command = container.get_dependency(UnnoteAttendanceForAllCommand)
            await command.execute()
