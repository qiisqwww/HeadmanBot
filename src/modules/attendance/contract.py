from abc import ABC, abstractmethod

from src.modules.common.domain import UniversityAlias

__all__ = [
    "AttendanceModuleContract",
]


class AttendanceModuleContract(ABC):
    @abstractmethod
    async def create_attendance(
        self,
        student_id: int,
        university_alias: UniversityAlias,
        group_id: int,
        group_name: str,
    ) -> None:
        ...

    @abstractmethod
    async def delete_attendance_by_student_id(self, student_id: int) -> None:
        ...

    @abstractmethod
    async def delete_attendance_by_lesson_id(self, lesson_id: int) -> None:
        ...

    @abstractmethod
    async def get_lessons_id_by_group_id(self, group_id: int) -> list[int] | None:
        ...

    @abstractmethod
    async def delete_lessons_by_group_id(self, group_id: int) -> None:
        ...
