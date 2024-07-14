import asyncio
from collections.abc import Callable

from aiogram import Bot
from celery import Celery

from src.modules.common.application import UseCase
from src.modules.common.infrastructure.config.config import BOT_TOKEN
from src.modules.common.infrastructure.container import Container

from .worker import worker


class TaskManager:
    _worker: Celery
    _tasks: list[Callable]

    def __init__(self) -> None:
        self._worker = worker
        self._tasks = []

    def add_task(self, action: UseCase, schedule: dict[str, str] | None = None) -> None:
        ...

    def run(self) -> None:
        ...

    def _create_task_callable(self, action: UseCase) -> Callable:
        def _wrapper() -> None:
            async def _async_wrapper() -> None:
                await Container.init(Bot(BOT_TOKEN))
                async with Container() as container:
                    command = container.get_dependency(action)
                    await command.execute()

            loop = asyncio.get_event_loop()
            loop.run_until_complete(_async_wrapper())

        return _wrapper
