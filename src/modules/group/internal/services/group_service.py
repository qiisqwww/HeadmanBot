from src.kernel.abstracts import AbstractStudent
from src.kernel.services import CorruptedDatabaseError, PostgresService
from src.modules.group.api.dto import Group
from src.modules.group.internal.gateways import UniversityGateway
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "GroupService",
]


class GroupService(PostgresService):
    async def find_by_name(self, name: str) -> Group | None:
        query = "SELECT * FROM groups.groups WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return Group.from_mapping(record)

    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> Group | None:
        university_gateway = UniversityGateway(self._con)
        university = await university_gateway.find_university_by_alias(university_alias)

        query = "SELECT * FROM groups.groups WHERE name LIKE $1 AND university_id = $2"
        record = await self._con.fetchrow(query, name, university.id)

        if record is None:
            return None

        return Group.from_mapping(record)

    async def get_by_student(self, student: AbstractStudent) -> Group:
        query = "SELECT group_id FROM groups.students_groups WHERE student_id = $1"
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
        query = "SELECT * FROM groups.groups"
        records = await self._con.fetch(query)

        return [Group.from_mapping(record) for record in records]

    async def create_or_return(self, name: str, headman_id: int, university_id: int) -> Group:
        found_group = await self.find_by_name(name)

        if found_group is not None:
            return found_group

        query = "INSERT INTO groups.groups (name, headman_id, university_id) VALUES ($1, $2, $3) RETURNING id"
        pk = await self._con.fetchval(query, name, headman_id, university_id)

        return Group(
            id=pk,
            name=name,
            headman_id=headman_id,
            university_id=university_id,
        )

    async def append_student_into_group(self, student: AbstractStudent, group: Group) -> None:
        query = "INSERT INTO groups.students_groups (student_id, group_id) VALUES($1, $2)"
        await self._con.execute(query, student.telegram_id, group.id)
