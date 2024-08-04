from abc import ABC, abstractmethod

from aiogram.types import User

__all__ = [
    "BotNotifier",
]


class BotNotifier(ABC):
    @abstractmethod
    async def notify_about_job_exception(self, exception: Exception, job_name: str) -> None:
        ...

    @abstractmethod
    async def notify_about_exception(self, exception: Exception, cause_by_student: User | None) -> None:
        ...
