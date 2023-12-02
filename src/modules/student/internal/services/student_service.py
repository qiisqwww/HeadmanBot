from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.kernel.student_dto import StudentDTO
from src.modules.student.internal.dto import StudentRawDTO
from src.modules.student.internal.gateways import GroupGateway, UniversityGatewate

__all__ = [
    "StudentService",
]


class StudentService(PostgresService):
    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._group_gateway = GroupGateway(con)
        self._university_gateway = UniversityGatewate(con)

    async def register_student(self, student_raw: StudentRawDTO) -> None:
        async with self._con.transaction():
            new_student = await self._create(student_raw)

            university = await self._university_gateway.find_university_by_alias(student_raw.university_alias)
            new_group = await self._group_gateway.create_or_return_group(
                student_raw.group_name,
                university.id,
            )

            await self._group_gateway.append_student_into_group(new_student, new_group)

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

    async def filter_by_group_name(self, group_name: str) -> list[StudentDTO]:
        students_id = await self._group_gateway.get_students_id_by_group_name(group_name)
        query = "SELECT * FROM students.students WHERE telegram_id IN $1"
        records = await self._con.fetch(query, students_id)

        return [StudentDTO.from_mapping(record) for record in records]

    async def _create(
        self,
        student_raw: StudentRawDTO,
    ) -> StudentDTO:
        query = "INSERT INTO students.students (telegram_id, name, surname, role) VALUES ($1, $2, $3, $4)"
        await self._con.execute(
            query,
            student_raw.telegram_id,
            student_raw.name,
            student_raw.surname,
            student_raw.role,
        )

        return StudentDTO(
            telegram_id=student_raw.telegram_id,
            name=student_raw.name,
            surname=student_raw.surname,
            role=student_raw.role,
        )
