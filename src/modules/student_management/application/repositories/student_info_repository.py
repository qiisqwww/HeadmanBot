from abc import abstractmethod

from src.modules.common.application.dependency import Dependency
from src.modules.student_management.domain import StudentInfo

__all__ = [
    "StudentInfoRepository",
]


class StudentInfoRepository(Dependency):
    @abstractmethod
    async def filter_by_group_id(self, group_id: int) -> list[StudentInfo]:
        ...
