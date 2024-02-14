from typing import final

from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import (
    StudentInfoRepository,
)
from src.modules.student_management.domain import StudentInfo

__all__ = [
    "GetStudentsInfoFromGroupQuery",
]


@final
class GetStudentsInfoFromGroupQuery(UseCase):
    _repository: StudentInfoRepository

    @inject
    def __init__(self, repository: StudentInfoRepository) -> None:
        self._repository = repository

    async def execute(self, group_id: int) -> list[StudentInfo]:
        return await self._repository.filter_by_group_id(group_id)
