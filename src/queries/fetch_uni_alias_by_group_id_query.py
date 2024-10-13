from typing import final

from injector import inject
from src.modules.edu_info.application.repositories import UniversityRepository

from src.common import UseCase
from src.dto.enums.university_alias import UniversityAlias

__all__ = [
    "FetchUniAliasByGroupIdQuery",
]


@final
class FetchUniAliasByGroupIdQuery(UseCase):
    _repository: UniversityRepository

    @inject
    def __init__(self, repository: UniversityRepository) -> None:
        self._repository = repository

    async def execute(self, group_id: int) -> UniversityAlias:
        return await self._repository.fetch_uni_alias_by_group_id(group_id)
