from typing import AsyncContextManager, Callable, final

from injector import Injector

from src.modules.common.application.jobs import AsyncJob
from src.modules.attendance.application.commands import MakeAttendanceRelevantCommand


@final 
class MakeAttendanceRelevantJob(AsyncJob):
    _build_container: Callable[[], AsyncContextManager[Injector]]

    def __init__(self, build_container: Callable[[], AsyncContextManager[Injector]], debug: bool) -> None:
        self._build_container = build_container

        if not debug:
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
