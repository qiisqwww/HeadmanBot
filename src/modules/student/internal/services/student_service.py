from src.modules.student.internal.dto import Student, StudentRaw
from src.modules.student.internal.gateways import GroupGateway, UniversityGatewate
from src.shared.abstract_dto import AbstractStudent
from src.shared.services import PostgresService

__all__ = [
    "StudentService",
]


class StudentService(PostgresService):
    async def register_student(self, student_raw: StudentRaw) -> None:
        async with self._con.transaction():
            group_gateway = GroupGateway(self._con)
            university_gateway = UniversityGatewate(self._con)
            new_student = await self._create(student_raw)

            university = await university_gateway.find_university_by_alias(student_raw.university_alias)
            new_group = await group_gateway.create_or_return_group(
                student_raw.group_name,
                student_raw.telegram_id,
                university.id,
            )

            await group_gateway.append_student_into_group(new_student, new_group)

    async def find(self, telegram_id: int) -> Student | None:
        query = "SELECT * FROM students.students WHERE telegram_id = $1"
        record = await self._con.fetchrow(query, telegram_id)

        if record is None:
            return None

        return Student.from_mapping(record)

    async def all(self) -> list[Student]:
        query = "SELECT * FROM students.students"
        records = await self._con.fetch(query)

        return [Student.from_mapping(record) for record in records]

    async def filter_by_group(self, group_id: int) -> list[Student]:
        # FIXME: Move to groups and delete join
        query = "SELECT * FROM groups.students_groups JOIN students ON student_id = telegram_id WHERE group_id = $1"
        records = await self._con.fetch(query, group_id)

        return [Student.from_mapping(record) for record in records]

    async def is_headman(self, student: AbstractStudent) -> bool:
        group_gateway = GroupGateway(self._con)
        headman_id = await group_gateway.get_headman_id(student)

        return headman_id == student.telegram_id

    async def _create(
        self,
        student_raw: StudentRaw,
    ) -> Student:
        query = "INSERT INTO students.students (telegram_id, name, surname, birthday, birthmonth) VALUES ($1, $2, $3, $4, $5)"
        await self._con.execute(
            query,
            student_raw.telegram_id,
            student_raw.name,
            student_raw.surname,
            student_raw.birthday,
            student_raw.birthmonth,
        )

        return Student(
            telegram_id=student_raw.telegram_id,
            name=student_raw.name,
            surname=student_raw.surname,
            birthday=student_raw.birthday,
            birthmonth=student_raw.birthmonth,
        )
