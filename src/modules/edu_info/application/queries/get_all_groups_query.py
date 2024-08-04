from injector import inject

from src.modules.common.application.use_case import UseCase
from src.modules.edu_info.application.repositories import GroupRepository
from src.modules.edu_info.domain import Group

__all__ = [
    "GetAllGroupsQuery",
]


class GetAllGroupsQuery(UseCase):
    _repository: GroupRepository

    @inject
    def __init__(self, repository: GroupRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[Group]:
        return await self._repository.all()
