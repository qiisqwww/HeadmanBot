from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.kernel.external.database.exceptions import CorruptedDatabaseError
from src.kernel.role import Role
from src.kernel.student_dto import GroupId, StudentDTO, StudentId
from src.modules.student.internal.dto import StudentRawDTO
from src.modules.student.internal.gateways import (
    AttendanceGateway,
    BirthdateGateway,
    GroupGateway,
    UniversityGatewate,
)

__all__ = [
    "StudentService",
]


class StudentService(PostgresService):
    _group_gateway: GroupGateway
    _university_gateway: UniversityGatewate
    _birthdate_gateway: BirthdateGateway
    _attendance_gateway: AttendanceGateway

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._group_gateway = GroupGateway(con)
        self._university_gateway = UniversityGatewate(con)
        self._birthdate_gateway = BirthdateGateway(con)
        self._attendance_gateway = AttendanceGateway(con)

    async def register_student(self, student_raw: StudentRawDTO) -> None:
        async with self._con.transaction():
            university = await self._university_gateway.get_university_by_alias(student_raw.university_alias)
            new_group = await self._group_gateway.create_or_return_group(
                student_raw.group_name,
                university.id,
            )

            new_student = await self._create(student_raw, new_group.id)

            await self._birthdate_gateway.create_birthdate(new_student.telegram_id, student_raw.birthdate)
            await self._attendance_gateway.create_attendances_for_student(new_student, new_group)

    async def find(self, telegram_id: int) -> StudentDTO | None:
        query = "SELECT * FROM students.students WHERE telegram_id = $1"
        record = await self._con.fetchrow(query, telegram_id)

        if record is None:
            return None

        return StudentDTO.from_mapping(record)

    async def all(self) -> list[StudentDTO]:
        query = "SELECT * FROM students.students"
        records = await self._con.fetch(query)

        return [StudentDTO.from_mapping(record) for record in records]

    async def get_headman_by_group_name(self, group_name: str) -> StudentDTO:
        group = await self._group_gateway.find_group_by_name(group_name)

        if group is None:
            raise CorruptedDatabaseError(f"Not found group with {group_name=}")

        query = "SELECT * FROM students.students WHERE group_id = $1 AND role LIKE $2"
        record = await self._con.fetchrow(query, group.id, Role.HEADMAN)

        if record is None:
            raise CorruptedDatabaseError(f"Not found headman for group with {group_name=}")

        return StudentDTO.from_mapping(record)

    async def group_has_headman(self, group_name) -> bool:
        group = await self._group_gateway.find_group_by_name(group_name)

        if group is None:
            return False

        query = "SELECT * FROM students.students WHERE group_id = $1 AND role LIKE $2"
        record = await self._con.fetchrow(query, group.id, Role.HEADMAN)

        return record is not None

    async def filter_by_group_name(self, group_name: str) -> list[StudentDTO]:
        group = await self._group_gateway.find_group_by_name(group_name)

        if group is None:
            raise CorruptedDatabaseError(f"Not found group with {group_name=}")

        query = "SELECT * FROM students.students WHERE group_id = $1"
        records = await self._con.fetch(query, group.id)

        return [StudentDTO.from_mapping(record) for record in records]

    async def _create(
        self,
        student_raw: StudentRawDTO,
        group_id: GroupId,
    ) -> StudentDTO:
        query = "INSERT INTO students.students (telegram_id, group_id, name, surname, role) VALUES ($1, $2, $3, $4, $5)"
        await self._con.execute(
            query,
            student_raw.telegram_id,
            group_id,
            student_raw.name,
            student_raw.surname,
            student_raw.role,
        )

        return StudentDTO(
            telegram_id=StudentId(student_raw.telegram_id),
            group_id=group_id,
            name=student_raw.name,
            surname=student_raw.surname,
            role=student_raw.role,
        )
