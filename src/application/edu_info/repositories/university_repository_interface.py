from abc import abstractmethod

from src.domain.edu_info import University, UniversityAlias

__all__ = [
    "UniversityRepository",
]


class UniversityRepository:
    @abstractmethod
    async def get_by_alias(self, alias: UniversityAlias) -> University:
        ...

    # @abstractmethod
    # async def all(self) -> list[University]:
    #     ...
    #
    # @abstractmethod
    # async def get_by_id(self, university_id: UniversityId) -> University:
    #     ...
    #
    # @abstractmethod
    # async def find_by_name(self, name: str) -> None | University:
    #     ...
    #
    # @abstractmethod
    # async def create(self, name: str, alias: UniversityAlias) -> None:
    #     ...
