from typing import final

from injector import inject

from src.modules.common.application import UseCase
from src.modules.edu_info.application.repositories import UniversityRepository

__all__ = [
    "FetchUniTimezonByGroupIdQuery",
]


@final
class FetchUniTimezonByGroupIdQuery(UseCase):
    _repository: UniversityRepository

    @inject
    def __init__(self, repository: UniversityRepository) -> None:
        self._repository= repository

    async def execute(self, group_id: int) -> str:
        return await self._repository.fetch_university_timezone_by_group_id(group_id)
