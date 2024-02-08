from abc import ABC, abstractmethod

from src.modules.common.domain import UniversityAlias
from src.modules.edu_info.domain import University

__all__ = [
    "UniversityRepository",
]


class UniversityRepository(ABC):
    @abstractmethod
    async def get_by_alias(self, alias: UniversityAlias) -> University:
        ...

    @abstractmethod
    async def all(self) -> list[University]:
        ...

    @abstractmethod
    async def create(self, name: str, alias: UniversityAlias, timezone: str) -> None:
        ...

    @abstractmethod
    async def find_by_name(self, name: str) -> None | University:
        ...

    @abstractmethod
    async def fetch_university_timezone_by_group_id(self, group_id: int) -> str:
        ...
