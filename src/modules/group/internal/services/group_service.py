from src.kernel.base import PostgresService
from src.kernel.external.database import CorruptedDatabaseError
from src.kernel.student_dto import StudentDTO
from src.modules.group.api.dto import GroupDTO
from src.modules.group.internal.gateways import UniversityGateway
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "GroupService",
]


class GroupService(PostgresService):
    async def find_by_name(self, name: str) -> GroupDTO | None:
        query = "SELECT * FROM groups.groups WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return GroupDTO.from_mapping(record)

    async def get_stundents_id_by_group_name(self, name: str) -> list[int]:
        query = "SELECT student_id FROM groups.students_groups JOIN groups.groups ON group_id = id WHERE name LIKE $1"
        records = await self._con.fetch(query, name)

        return [record["student_id"] for record in records]

    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> GroupDTO | None:
        university_gateway = UniversityGateway(self._con)
        university = await university_gateway.find_university_by_alias(university_alias)

        query = "SELECT * FROM groups.groups WHERE name LIKE $1 AND university_id = $2"
        record = await self._con.fetchrow(query, name, university.id)

        if record is None:
            return None

        return GroupDTO.from_mapping(record)

    async def get_by_student(self, student: StudentDTO) -> GroupDTO:
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

        return GroupDTO.from_mapping(record)

    async def all(self) -> list[GroupDTO]:
        query = "SELECT * FROM groups.groups"
        records = await self._con.fetch(query)

        return [GroupDTO.from_mapping(record) for record in records]

    async def create_or_return(self, name: str, university_id: int) -> GroupDTO:
        found_group = await self.find_by_name(name)

        if found_group is not None:
            return found_group

        query = "INSERT INTO groups.groups (name, university_id) VALUES ($1, $2) RETURNING id"
        pk = await self._con.fetchval(query, name, university_id)

        return GroupDTO(
            id=pk,
            name=name,
            university_id=university_id,
        )

    async def append_student_into_group(self, student: StudentDTO, group: GroupDTO) -> None:
        query = "INSERT INTO groups.students_groups (student_id, group_id) VALUES($1, $2)"
        await self._con.execute(query, student.telegram_id, group.id)
