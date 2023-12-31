from abc import abstractmethod

from src.dto.models import University, UniversityId
from src.enums import UniversityAlias
from src.repositories import UniversityRepository

from .service import Service

__all__ = [
    "UniversityService",
]


class UniversityService(Service):
    @abstractmethod
    def __init__(self, university_repository: UniversityRepository) -> None:
        ...

    @abstractmethod
    async def add_universities(self) -> None:
        ...

    @abstractmethod
    async def all(self) -> list[University]:
        ...

    @abstractmethod
    async def get_by_alias(self, alias: UniversityAlias) -> University:
        ...

    @abstractmethod
    async def get_by_id(self, university_id: UniversityId) -> University:
        ...
