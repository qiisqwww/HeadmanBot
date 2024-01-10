from abc import ABC, abstractmethod

from src.modules.common.domain import UniversityAlias

__all__ = [
    "AttendanceModuleContract",
]


class AttendanceModuleContract(ABC):
    @abstractmethod
    async def create_attendance(
        self, student_id: int, university_alias: UniversityAlias, group_id: int, group_name: str
    ) -> None:
        ...
