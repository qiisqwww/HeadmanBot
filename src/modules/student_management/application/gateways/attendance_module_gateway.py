from abc import ABC, abstractmethod

from src.modules.attendance.application.contract import AttendanceModuleContract
from src.modules.common.domain import UniversityAlias

__all__ = [
    "AttendanceModuleGateway",
]


class AttendanceModuleGateway(ABC):
    _contract: AttendanceModuleContract

    @abstractmethod
    async def create_attendance(
        self, student_id: int, university_alias: UniversityAlias, group_id: int, group_name: str
    ) -> None:
        ...
