from abc import ABC, abstractmethod

from src.modules.student_management.domain import Role, StudentInfo

__all__ = [
    "StudentInfoRepository",
]


class StudentInfoRepository(ABC):
    @abstractmethod
    async def filter_by_group_id(self, group_id: int) -> list[StudentInfo]:
        ...

    async def get_role_by_telegram_id(self, telegram_id: int) -> Role:
        ...
