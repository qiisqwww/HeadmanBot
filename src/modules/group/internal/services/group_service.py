from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.kernel.external.database import CorruptedDatabaseError
from src.modules.group.api.dto import GroupDTO, GroupId
from src.modules.group.internal.gateways import UniversityGateway
from src.modules.university.api.dto import UniversityId
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "GroupService",
]


class GroupService(PostgresService):
    _university_gateway: UniversityGateway

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._university_gateway = UniversityGateway(con)

    async def find_by_name(self, name: str) -> GroupDTO | None:
        query = "SELECT * FROM groups.groups WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return GroupDTO.from_mapping(record)

    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> GroupDTO | None:
        university = await self._university_gateway.get_university_by_alias(university_alias)

        query = "SELECT * FROM groups.groups WHERE name LIKE $1 AND university_id = $2"
        record = await self._con.fetchrow(query, name, university.id)

        if record is None:
            return None

        return GroupDTO.from_mapping(record)

    async def get_by_id(self, group_id: GroupId) -> GroupDTO:
        query = "SELECT * FROM groups.groups WHERE id = $1"
        record = await self._con.fetchrow(query, group_id)

        if record is None:
            raise CorruptedDatabaseError(f"Group with id={group_id} does not exists.")

        return GroupDTO.from_mapping(record)

    async def all(self) -> list[GroupDTO]:
        query = "SELECT * FROM groups.groups"
        records = await self._con.fetch(query)

        return [GroupDTO.from_mapping(record) for record in records]

    async def create_or_return(self, name: str, university_id: UniversityId) -> GroupDTO:
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
