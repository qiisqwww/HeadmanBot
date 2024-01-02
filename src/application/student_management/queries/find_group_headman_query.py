from src.domain.edu_info import Group
from src.domain.student_management import Role, Student

from ..repositories import StudentRepository

__all__ = [
    "FindGroupHeadmanQuery",
]


class FindGroupHeadmanQuery:
    _repository: StudentRepository

    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, group: Group) -> Student | None:
        return await self._repository.find_by_group_id_and_role(group.id, Role.HEADMAN)
