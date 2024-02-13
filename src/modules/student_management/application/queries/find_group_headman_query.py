from typing import final

from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.domain import Role, Student

from ..repositories import StudentRepository

__all__ = [
    "FindGroupHeadmanQuery",
]


@final
class FindGroupHeadmanQuery(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, group_id: int) -> Student:
        headman = await self._repository.find_by_group_id_and_role(
            group_id, Role.HEADMAN,
        )

        if headman is None:
            raise RuntimeError("Not found headman for group.")

        return headman
