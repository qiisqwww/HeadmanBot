from src.dto import Group, Student

from .exceptions import CorruptedDatabaseError
from .service import Service

__all__ = [
    "GroupService",
]


class GroupService(Service):
    async def get_by_name(self, name: str) -> Group | None:
        query = "SELECT * FROM groups WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return Group.from_mapping(record)

    async def get_by_pk(self, pk: int) -> Group | None:
        query = "SELECT * FROM groups WHERE id = $1"
        record = await self._con.fetchrow(query, pk)

        if record is None:
            return None

        return Group.from_mapping(record)

    async def get_by_student(self, student: Student) -> Group:
        query = "SELECT group_id FROM students_group WHERE student_id = $1"
        group_id = await self._con.fetchval(query, student.telegram_id)

        if group_id is None:
            raise CorruptedDatabaseError(
                f"Group for student with id={student.telegram_id} {student.surname} {student.name} does not exists."
            )

        query = "SELECT * FROM groups WHERE id = $1"
        record = await self._con.fetchrow(query, group_id)

        if record is None:
            raise CorruptedDatabaseError(
                f"Group for student with id={student.telegram_id} {student.surname} {student.name} does not exists."
            )

        return Group.from_mapping(record)

    async def all(self) -> list[Group]:
        query = "SELECT * FROM groups"
        records = await self._con.fetch(query)

        return [Group.from_mapping(record) for record in records]

    async def append_student_to_group(self, group: Group, student: Student) -> None:
        query = "INSER INTO students_group (student_id, group_id) VALUES($1, $2)"
        await self._con.execute(query, student.telegram_id, group.id)

    async def create(self, name: str, headman_id: int, university_id: int) -> Group:
        query = "INSERT INTO groups (name, headman_id, university_id) VALUES ($1, $2, $3) RETURNING id"
        pk = await self._con.fetchval(query, name)

        return Group(
            id=pk,
            name=name,
            headman_id=headman_id,
            university_id=university_id,
        )
