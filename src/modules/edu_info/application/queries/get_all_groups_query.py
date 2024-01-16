from src.modules.common.application import Dependency
from src.modules.edu_info.application.repositories import GroupRepository

from ...domain import Group

__all__ = [
    "GetAllGroupsQuery",
]


class GetAllGroupsQuery(Dependency):
    _repository: GroupRepository

    def __init__(self, repository: GroupRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[Group]:
        return await self._repository.all()
