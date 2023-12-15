from src.dto import Student, StudentRaw
from src.repositories import StudentRepository
from src.services import StudentService, GroupService
from src.repositories.exceptions import CorruptedDatabaseError
from src.dto import GroupId

__all__ = [
    "StudentServiceImpl",
]


class StudentServiceImpl(StudentService):
    _student_repository: StudentRepository
    _group_service: GroupService

    def __init__(
        self,
        student_repository: StudentRepository,
    ) -> None:
        self._student_repository = student_repository

    async def find(self, telegram_id: int) -> Student | None:
        return await self._student_repository.find(telegram_id)

    async def all(self) -> list[Student]:
        return await self._student_repository.all()

    # async def get_headman_by_group_name(self, group_name: str) -> Student:
    #     group = await self._group_gateway.find_group_by_name(group_name)
    #
    #     if group is None:
    #         raise CorruptedDatabaseError(f"Not found group with {group_name=}")
    #
    #     query = "SELECT * FROM students.students WHERE group_id = $1 AND role LIKE $2"
    #     record = await self._con.fetchrow(query, group.id, Role.HEADMAN)
    #
    #     if record is None:
    #         raise CorruptedDatabaseError(f"Not found headman for group with {group_name=}")
    #
    #     return Student.from_mapping(record)

    # async def group_has_headman(self, group_name) -> bool:
    #     group = await self._group_gateway.find_group_by_name(group_name)
    #
    #     if group is None:
    #         return False
    #
    #     query = "SELECT * FROM students.students WHERE group_id = $1 AND role LIKE $2"
    #     record = await self._con.fetchrow(query, group.id, Role.HEADMAN)
    #
    #     return record is not None

    async def filter_by_group_id(self, group_id: GroupId) -> list[Student] | None:
        if group_id is None:
            raise CorruptedDatabaseError(f"Not found group with {group_id=}")

        return await self._student_repository.filter_group_by_id(group_id)

    async def register_student(self, student: StudentRaw) -> None:
        group = await self._group_service.find_by_name(student.group_name)
        new_student = await self._student_repository.create_and_return(student, group.id)

        if new_student is None:
            raise CorruptedDatabaseError(f"Got some mistakes while registratig user {student.telegram_id}")

