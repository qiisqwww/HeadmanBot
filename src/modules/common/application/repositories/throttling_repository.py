from abc import abstractmethod

from src.modules.common.application import Dependency


class ThrottlingRepository(Dependency):

    @abstractmethod
    async def increase_user_throttling_rate(self, user_id: str) -> int:
        ...

    @abstractmethod
    async def set_execution_time(self, user_id: str) -> None:
        ...
