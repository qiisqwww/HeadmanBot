from src.dto import Group, GroupId, UniversityId
from src.enums import UniversityAlias

from ..exceptions import CorruptedDatabaseError
from ..interfaces import GroupRepository
from .postgres_repository import PostgresRepositoryImpl

__all__ = [
    "GroupRepositoryImpl",
]


class GroupRepositoryImpl(PostgresRepositoryImpl, GroupRepository):
    async def find_by_name(self, name: str) -> Group | None:
        query = "SELECT * FROM groups WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return Group.from_mapping(record)

    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> Group | None:
        query = (
            "SELECT gr.id, gr.name, gr.university_id "
            "FROM groups gr "
            "JOIN universities AS un "
            "ON gr.university_id = un.id "
            "WHERE gr.name LIKE $1 AND un.alias LIKE $2"
        )

        record = await self._con.fetchrow(query, name, university_alias)

        if record is None:
            return None

        return Group.from_mapping(record)

    async def get_by_id(self, group_id: GroupId) -> Group:
        query = "SELECT * FROM groups WHERE id = $1"
        record = await self._con.fetchrow(query, group_id)

        if record is None:
            raise CorruptedDatabaseError(f"Group with id={group_id} does not exists.")

        return Group.from_mapping(record)

    async def all(self) -> list[Group] | None:
        query = "SELECT * FROM groups"
        records = await self._con.fetch(query)

        if records is None:
            raise CorruptedDatabaseError(f"There are no groups in table")

        return [Group.from_mapping(record) for record in records]

    async def create(self, name: str, university_id: UniversityId) -> Group:
        query = "INSERT INTO groups (name, university_id) VALUES ($1, $2) RETURNING id"
        pk = await self._con.fetchval(query, name, university_id)

        return Group(
            id=pk,
            name=name,
            university_id=university_id,
        )
