from abc import ABC, abstractmethod

from src.modules.student_management.domain import StudentInfo

__all__ = [
    "StudentInfoRepository",
]


class StudentInfoRepository(ABC):
    @abstractmethod
    async def filter_by_group_id(self, group_id: int) -> list[StudentInfo]:
        ...
