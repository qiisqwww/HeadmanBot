from abc import abstractmethod

from src.modules.common.application import Dependency


class ThrottlingRepository(Dependency):
    @abstractmethod
    async def set_user_throttling(self, user_id: str) -> None:
        ...

    @abstractmethod
    async def increase_user_throttling(self, user_id: str) -> None:
        ...

    @abstractmethod
    async def get_user_throttling(self, user_id: str) -> int | None:
        ...
