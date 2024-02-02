from abc import abstractmethod

from src.modules.common.application import Dependency

__all__ = [
    "ThrottlingRepository"
]


class ThrottlingRepository(Dependency):

    @abstractmethod
    async def increase_user_throttling_rate(self, user_id: str) -> int:
        ...

    @abstractmethod
    async def set_expire_time(self, user_id: str) -> None:
        ...
