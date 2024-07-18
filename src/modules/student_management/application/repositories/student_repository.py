from abc import ABC, abstractmethod
from datetime import date

from src.modules.student_management.domain import Role, Student

from .create_student_dto import CreateStudentDTO
from .student_enter_group_dto import StudentEnterGroupDTO

__all__ = [
    "StudentRepository",
]


class StudentRepository(ABC):
    @abstractmethod
    async def find_by_id(self, student_id: int) -> Student | None:
        ...

    @abstractmethod
    async def find_by_telegram_id(self, telegram_id: int) -> Student | None:
        ...

    @abstractmethod
    async def find_by_group_id_and_role(
        self,
        group_id: int,
        role: Role,
    ) -> Student | None:
        ...

    @abstractmethod
    async def filter_by_group_id(
        self,
        group_id: int,
    ) -> list[Student]:
        ...

    @abstractmethod
    async def find_by_fullname_and_group_id(
        self,
        last_name: str,
        first_name: str,
        group_id: int,
    ) -> Student | None:
        ...

    @abstractmethod
    async def create(
        self,
        student_data: CreateStudentDTO,
        group_id: int,
    ) -> Student:
        ...

    @abstractmethod
    async def update_attendance_noted_by_id(
        self,
        student_id: int,
        new_attendance_noted: bool,
    ) -> None:
        ...

    @abstractmethod
    async def update_attendance_noted_all(self, new_attendance_noted: bool) -> None:
        ...

    @abstractmethod
    async def update_first_name_by_id(
        self,
        student_id: int,
        new_first_name: str,
    ) -> None:
        ...

    @abstractmethod
    async def update_last_name_by_id(self, student_id: int, new_last_name: str) -> None:
        ...

    @abstractmethod
    async def update_birthdate_by_id(
        self,
        student_id: int,
        new_birthdate: date | None,
    ) -> None:
        ...

    @abstractmethod
    async def get_students_count(self) -> int:
        ...

    @abstractmethod
    async def get_active_students_count(self) -> int:
        ...

    @abstractmethod
    async def delete_by_telegram_id(self, telegram_id: int) -> None:
        ...

    @abstractmethod
    async def delete_by_fullname_and_group_id(
        self,
        first_name: str,
        last_name: str,
        group_id: int,
    ) -> None:
        ...

    @abstractmethod
    async def delete_all_by_group_id(self, group_id: int) -> None:
        ...

    @abstractmethod
    async def set_role_by_id(self, student_id: int, role: Role) -> None:
        ...

    @abstractmethod
    async def expel_user_from_group_by_id(self, student_id: int) -> None:
        ...

    @abstractmethod
    async def enter_group_by_telegram_id(self, student_data: StudentEnterGroupDTO, group_id: int) -> None:
        ...
