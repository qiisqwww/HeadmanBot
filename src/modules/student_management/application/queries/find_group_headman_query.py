from injector import inject

from src.modules.common.application.dependency import Dependency
from src.modules.student_management.domain import Role, Student

from ..repositories import StudentRepository

__all__ = [
    "FindGroupHeadmanQuery",
]


class FindGroupHeadmanQuery(Dependency):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, group_name: str) -> Student | None:
        return await self._repository.find_by_group_name_and_role(group_name, Role.HEADMAN)
