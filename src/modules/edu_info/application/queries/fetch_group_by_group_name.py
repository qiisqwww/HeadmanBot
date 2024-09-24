from typing import final

from injector import inject

from src.modules.common.application import UseCase
from src.modules.edu_info.domain import Group
from src.modules.edu_info.application.repositories import GroupRepository

__all__ = [
    "FetchGroupByGroupName",
]


@final
class FetchGroupByGroupName(UseCase):
    _repository: GroupRepository

    @inject
    def __init__(self, repository: GroupRepository) -> None:
        self._repository = repository

    async def execute(self, group_name: str) -> Group | None:
        return await self._repository.find_by_name(group_name)
