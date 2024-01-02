from src.application.edu_info.repositories import GroupRepository
from src.domain.edu_info import UniversityAlias

__all__ = [
    "IsGroupRegisteredQuery",
]


class IsGroupRegisteredQuery:
    _repository: GroupRepository

    def __init__(self, repository: GroupRepository) -> None:
        self._repository = repository

    async def execute(self, group_name: str, university_alias: UniversityAlias) -> bool:
        return (await self._repository.find_by_name_and_uni(group_name, university_alias)) is not None
