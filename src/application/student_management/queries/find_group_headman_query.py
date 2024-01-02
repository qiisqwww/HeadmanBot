from src.domain.student_management import Role, Student

from ..repositories import StudentRepository

__all__ = [
    "FindGroupHeadmanQuery",
]


class FindGroupHeadmanQuery:
    _repository: StudentRepository

    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, group_name: str) -> Student | None:
        return await self._repository.find_by_group_name_and_role(group_name, Role.HEADMAN)
