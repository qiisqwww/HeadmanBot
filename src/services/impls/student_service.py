from src.dto.models import (
    GroupId,
    Student,
    StudentLoginData,
    University
)
from src.enums import Role
from src.repositories import StudentRepository
from src.repositories.exceptions import CorruptedDatabaseError
from src.services import (
    GroupService,
    StudentService,
    UniversityService
)

__all__ = [
    "StudentServiceImpl",
]


class StudentServiceImpl(StudentService):
    _student_repository: StudentRepository
    _group_service: GroupService
    _university_service: UniversityService

    def __init__(
        self, student_repository: StudentRepository, group_service: GroupService, university_service: UniversityService
    ) -> None:
        self._student_repository = student_repository
        self._group_service = group_service
        self._university_service = university_service

    async def find(self, telegram_id: int) -> Student | None:
        return await self._student_repository.find_by_id(telegram_id)

    async def all(self) -> list[Student]:
        return await self._student_repository.all()

    async def get_headman_by_group_name(self, group_name: str) -> Student | None:
        group = await self._group_service.find_by_name(group_name)

        if group is None:
            raise CorruptedDatabaseError(f"Not found group with {group_name=}")

        headman = await self._student_repository.find_by_group_id_and_role(group.id, Role.HEADMAN)

        if headman is None:
            raise CorruptedDatabaseError(f"Not found headman for group with {group_name=}")

        return headman

    async def filter_by_group_id(self, group_id: GroupId) -> list[Student] | None:
        if group_id is None:
            raise CorruptedDatabaseError(f"Not found group with {group_id=}")

        return await self._student_repository.filter_group_by_id(group_id)

    async def register_student(self, student: StudentLoginData) -> None:
        university: University = await self._university_service.get_by_alias(student.university_alias)

        group = await self._group_service.create_or_return(student.group_name, university.id)

        if group is None:
            raise CorruptedDatabaseError(f"Group {student.group_name} does not exists and was not created")

        new_student = await self._student_repository.create_and_return(student, group.id)

        if new_student is None:
            raise CorruptedDatabaseError(f"Got some mistakes while registratig user {student.telegram_id}")
