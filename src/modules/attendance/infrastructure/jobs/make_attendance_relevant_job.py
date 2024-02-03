from typing import AsyncContextManager, Callable, final

from injector import Injector

from src.modules.common.infrastructure.scheduling import AsyncJob
from src.modules.attendance.application.commands import MakeAttendanceRelevantCommand
from src.modules.common.infrastructure.config import DEBUG

__all__ = [
    "MakeAttendanceRelevantJob",
]

@final 
class MakeAttendanceRelevantJob(AsyncJob):
    _build_container: Callable[[], AsyncContextManager[Injector]]

    def __init__(self, build_container: Callable[[], AsyncContextManager[Injector]]) -> None:
        self._build_container = build_container

        if not DEBUG:
            self._trigger = "cron"
            self._trigger_args = {
                "hour": 1,
                "minute": 00,
                "day_of_week": "mon-sat",
            }

    async def __call__(self) -> None:
        async with self._build_container() as container:
            command = container.get(MakeAttendanceRelevantCommand)
            await command.execute()
