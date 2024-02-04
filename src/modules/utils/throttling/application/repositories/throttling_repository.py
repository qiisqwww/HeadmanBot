from abc import ABC, abstractmethod

__all__ = [
    "ThrottlingRepository",
]


class ThrottlingRepository(ABC):
    @abstractmethod
    async def increase_user_throttling_rate(self, user_id: str) -> int:
        ...

    @abstractmethod
    async def set_expire_time(self, user_id: str) -> None:
        ...
