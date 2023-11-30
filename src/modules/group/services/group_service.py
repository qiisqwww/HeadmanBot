from src.dto import Group, Student
from src.shared.services import CorruptedDatabaseError, PostgresService

__all__ = [
    "GroupService",
]


class GroupService(PostgresService):
    async def find_by_name(self, name: str) -> Group | None:
        query = "SELECT * FROM groups WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return Group.from_mapping(record)

    async def find_by_name_and_uni(self, name: str, university_id: int) -> Group | None:
        query = "SELECT * FROM groups WHERE name LIKE $1 AND university_id = $2"
        record = await self._con.fetchrow(query, name, university_id)

        if record is None:
            return None

        return Group.from_mapping(record)

    async def get_by_student(self, student: Student) -> Group:
        query = "SELECT group_id FROM students_groups WHERE student_id = $1"
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

    async def create_or_return(self, name: str, headman_id: int, university_id: int) -> Group:
        found_group = await self.find_by_name(name)

        if found_group is not None:
            return found_group

        query = "INSERT INTO groups (name, headman_id, university_id) VALUES ($1, $2, $3,) RETURNING id"
        pk = await self._con.fetchval(query, name, headman_id, university_id)

        return Group(
            id=pk,
            name=name,
            headman_id=headman_id,
            university_id=university_id,
        )

    async def append_student_into_group(self, student: Student, group: Group) -> None:
        query = "INSERT INTO students_groups (student_id, group_id) VALUES($1, $2)"
        await self._con.execute(query, student.telegram_id, group.id)
