from typing import final

from injector import inject

from src.modules.common.application import UseCase
from src.modules.common.domain.university_alias import UniversityAlias
from src.modules.edu_info.application.repositories import UniversityRepository

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
