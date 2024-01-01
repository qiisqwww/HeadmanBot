from src.application.edu_info.repositories import UniversityRepository
from src.domain.edu_info import University, UniversityAlias

__all__ = [
    "GetUniversityByAliasQuery",
]


class GetUniversityByAliasQuery:
    _repository: UniversityRepository

    def __init__(self, repository: UniversityRepository) -> None:
        self._repository = repository

    async def execute(self, alias: UniversityAlias) -> University:
        return await self._repository.get_by_alias(alias)
