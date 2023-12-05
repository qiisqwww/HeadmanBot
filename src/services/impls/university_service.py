from src.config import UNIVERSITIES_LIST
from src.dto import University, UniversityId
from src.enums import UniversityAlias
from src.repositories import UniversityRepository

from ..interfaces import UniversityService

__all__ = [
    "UniversityServiceImpl",
]


class UniversityServiceImpl(UniversityService):
    _university_repository: UniversityRepository

    def __init__(self, university_repository: UniversityRepository) -> None:
        self._university_repository = university_repository

    async def add_universities(self) -> None:
        for name, alias in UNIVERSITIES_LIST:
            await self._try_create(name, alias)

    async def all(self) -> list[University]:
        return await self._university_repository.all()

    async def get_by_alias(self, alias: UniversityAlias) -> University:
        return await self._university_repository.get_by_alias(alias)

    async def get_by_id(self, university_id: UniversityId) -> University:
        return await self._university_repository.get_by_id(university_id)

    async def _try_create(self, name: str, alias: UniversityAlias) -> None:
        """Trying create new university if is does not exists."""

        found_university = await self._university_repository.find_by_name(name)

        if found_university is not None:
            return

        await self._university_repository.create(name, alias)
